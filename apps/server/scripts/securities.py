import argparse
import asyncio
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy import select

from axiom.db.client import AsyncSessionLocal
from axiom.db.models import (
    AssetSubType,
    AssetType,
    Exchange,
    Security,
    StreamSubscription,
)
from axiom.env import env
from axiom.mdata import SchwabAuthService


def _chunks(items: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _normalize_asset_type(value: Optional[str]) -> AssetType:
    v = (value or "").upper()
    try:
        return AssetType(v)  # type: ignore[arg-type]
    except Exception:
        return AssetType.EQUITY


def _normalize_asset_subtype(value: Optional[str]) -> Optional[AssetSubType]:
    if not value:
        return None
    v = value.upper()
    try:
        return AssetSubType(v)  # type: ignore[arg-type]
    except Exception:
        return None


EXCHANGE_PRESETS: Dict[str, Dict[str, str]] = {
    "NASDAQ": {"mic": "XNAS", "name": "NASDAQ", "tz": "America/New_York"},
    "NYSE": {
        "mic": "XNYS",
        "name": "New York Stock Exchange",
        "tz": "America/New_York",
    },
    "ARCA": {"mic": "ARCX", "name": "NYSE Arca", "tz": "America/New_York"},
}


def _pick_exchange_code(item: Dict[str, Any]) -> str:
    f = item.get("fundamental") or {}
    code = (
        f.get("exchange")
        or f.get("exchangeName")
        or item.get("exchange")
        or item.get("exchangeName")
        or "NASDAQ"
    )
    return str(code).upper()


async def _ensure_exchange(exchange_code: str) -> Exchange:
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Exchange).where(Exchange.code == exchange_code))
        ex = res.scalar_one_or_none()
        if ex:
            return ex
        preset = EXCHANGE_PRESETS.get(exchange_code, None)
        if preset is None:
            preset = {"mic": "XXXX", "name": exchange_code, "tz": "Etc/UTC"}
        ex = Exchange(
            code=exchange_code,
            name=preset["name"],
            mic_code=preset["mic"],
            timezone=preset["tz"],
            currency="USD",
            is_active=True,
        )
        db.add(ex)
        await db.commit()
        await db.refresh(ex)
        return ex


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def _to_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    try:
        s = str(value).strip().lower()
        if s in ("true", "1", "yes", "y"):  # pragma: no cover - trivial
            return True
        if s in ("false", "0", "no", "n"):
            return False
    except Exception:
        pass
    return None


async def upsert_security_from_item(item: Dict[str, Any]) -> Optional[Security]:
    symbol = (item.get("symbol") or item.get("SYMBOL") or "").upper()
    if not symbol:
        return None

    f = item.get("fundamental") or {}
    description = f.get("description") or item.get("description") or symbol
    cusip = f.get("cusip") or item.get("cusip")
    has_options = _to_bool(f.get("optionable") or item.get("optionable")) or False
    is_shortable = _to_bool(f.get("shortable") or item.get("shortable"))
    is_htb = _to_bool(f.get("isHardToBorrow") or item.get("isHardToBorrow"))
    htb_rate = f.get("htbRate") or item.get("htbRate")
    market_cap = _coerce_int(f.get("marketCap") or item.get("marketCap"))
    shares_out = _coerce_int(
        f.get("sharesOutstanding") or item.get("sharesOutstanding")
    )
    sector = f.get("sector") or item.get("sector")
    industry = f.get("industry") or item.get("industry")
    asset_type = _normalize_asset_type(f.get("assetType") or item.get("assetType"))
    asset_sub_type = _normalize_asset_subtype(
        f.get("assetSubType") or item.get("assetSubType")
    )

    exchange_code = _pick_exchange_code(item)
    exchange = await _ensure_exchange(exchange_code)

    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Security).where(Security.symbol == symbol))
        sec = res.scalar_one_or_none()
        if sec is None:
            sec = Security(
                symbol=symbol,
                description=str(description)[:255],
                exchange_id=exchange.id,
                asset_type=asset_type,  # type: ignore[arg-type]
                asset_sub_type=asset_sub_type,  # type: ignore[arg-type]
                sector=sector,
                industry=industry,
                market_cap=market_cap,
                shares_outstanding=shares_out,
                is_shortable=is_shortable,
                is_hard_to_borrow=is_htb,
                htb_rate=htb_rate,
                has_options=bool(has_options),
                is_active=True,
                cusip=cusip,
            )
            db.add(sec)
        else:
            sec.description = str(description)[:255]
            sec.exchange_id = exchange.id
            sec.asset_type = asset_type  # type: ignore[assignment]
            sec.asset_sub_type = asset_sub_type  # type: ignore[assignment]
            sec.sector = sector
            sec.industry = industry
            sec.market_cap = market_cap
            sec.shares_outstanding = shares_out
            sec.is_shortable = is_shortable
            sec.is_hard_to_borrow = is_htb
            sec.htb_rate = htb_rate
            sec.has_options = bool(has_options)
            if cusip:
                sec.cusip = cusip
            sec.is_active = True
        await db.commit()
        await db.refresh(sec)
        return sec


async def collect_symbols_from_subscriptions(user_id: str) -> List[str]:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(StreamSubscription.symbol)
            .where(StreamSubscription.user_id == user_id)
            .where(StreamSubscription.is_active)
        )
        symbols = [row[0].upper() for row in result.fetchall() if row[0]]
        return sorted(list(set(symbols)))


async def upsert_securities_for_user(user_id: str, chunk_size: int = 50) -> int:
    auth = SchwabAuthService()
    client = await auth.get_client_for_user(user_id)
    if client is None:
        print("No Schwab client available for this user. Complete OAuth first.")
        return 0

    symbols = await collect_symbols_from_subscriptions(user_id)
    if not symbols:
        print("No active subscriptions found; nothing to sync.")
        return 0

    def _flatten_instruments_payload(payload: Any) -> List[Dict[str, Any]]:
        flat: List[Dict[str, Any]] = []
        # The Schwab API may return {"AAPL": {...}} or {"AAPL": [{...}, {...}]}
        # or a list of dicts. Normalize to list[dict].
        values: List[Any]
        if isinstance(payload, dict):
            values = list(payload.values())
        elif isinstance(payload, list):
            values = payload
        else:
            values = []

        for v in values:
            if isinstance(v, dict):
                flat.append(v)
            elif isinstance(v, list):
                for vv in v:
                    if isinstance(vv, dict):
                        flat.append(vv)
        return flat

    total = 0
    for group in _chunks(symbols, chunk_size):
        resp = await client.get_instruments(
            group, client.Instrument.Projection.FUNDAMENTAL
        )
        resp.raise_for_status()
        data = resp.json() or []
        for item in _flatten_instruments_payload(data):
            sec = await upsert_security_from_item(item)
            if sec is not None:
                total += 1
    return total


async def main_async() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and store Security metadata for all subscribed symbols"
    )
    parser.add_argument(
        "--user-id",
        required=False,
        default=env.OWNER_ID,
        help="User ID whose subscriptions will be read (default: env.OWNER_ID)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=50,
        help="Batch size for instrument fundamentals API calls (default: 50)",
    )
    args = parser.parse_args()

    total = await upsert_securities_for_user(args.user_id, chunk_size=args.chunk_size)
    print(f"Upserted {total} securities from subscriptions for user {args.user_id}.")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
