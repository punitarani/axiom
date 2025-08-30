import argparse
import asyncio
from datetime import datetime, timezone
from typing import Iterable, List, Optional

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.db.client import AsyncSessionLocal
from axiom.db.models.subscription import StreamSubscription
from axiom.env import env

DEFAULT_TICKERS: List[str] = [
    "AAPL",
    "ABBV",
    "ABT",
    "ADBE",
    "AMD",
    "AMGN",
    "AMZN",
    "ASML",
    "AVGO",
    "AXP",
    "BA",
    "BABA",
    "BAC",
    "BKNG",
    "C",
    "CAT",
    "COP",
    "CRM",
    "CVX",
    "DE",
    "DIA",
    "DIS",
    "DOCU",
    "EEM",
    "EWZ",
    "F",
    "GILD",
    "GIS",
    "GLD",
    "GM",
    "GOOGL",
    "GS",
    "HD",
    "INTC",
    "ISRG",
    "IVV",
    "IWM",
    "JNJ",
    "JPM",
    "KO",
    "LMT",
    "LOW",
    "MA",
    "MCD",
    "META",
    "MRK",
    "MRVL",
    "MS",
    "MSFT",
    "MU",
    "NFLX",
    "NIO",
    "NKE",
    "NVDA",
    "ORCL",
    "PFE",
    "PLTR",
    "PYPL",
    "QQQ",
    "QQQM",
    "REGN",
    "RIVN",
    "ROKU",
    "RTX",
    "SBUX",
    "SLV",
    "SMH",
    "SNAP",
    "SNOW",
    "SOXX",
    "SPY",
    "SQ",
    "T",
    "TGT",
    "TLT",
    "TSLA",
    "UBER",
    "V",
    "VOO",
    "VZ",
    "WFC",
    "WMT",
    "XBI",
    "XLE",
    "XLF",
    "XOM",
    "XOP",
    "YUM",
    "ZM",
    "ZS",
]


def _parse_symbols(value: Optional[str]) -> List[str]:
    if not value:
        return DEFAULT_TICKERS
    symbols: List[str] = [s.strip().upper() for s in value.split(",") if s.strip()]
    return symbols or DEFAULT_TICKERS


async def clear_subscriptions(user_id: str) -> None:
    """Clear all existing subscriptions for the user."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            delete(StreamSubscription).where(StreamSubscription.user_id == user_id)
        )
        await db.commit()
        deleted_count = result.rowcount or 0
    print(f"Cleared {deleted_count} existing subscriptions for user {user_id}")


async def bulk_add_subscriptions(
    db: AsyncSession,
    user_id: str,
    stream_type: str,
    symbols: List[str],
    book: Optional[str] = None,
    is_active: bool = True,
) -> int:
    """Bulk add/update subscriptions using PostgreSQL's INSERT ... ON CONFLICT."""
    if not symbols:
        return 0

    # Prepare bulk insert data
    now = datetime.now(timezone.utc)
    subscription_data = [
        {
            "user_id": user_id,
            "symbol": symbol.upper(),
            "stream_type": stream_type,
            "book": book,
            "is_active": is_active,
            "created_at": now,
        }
        for symbol in symbols
    ]

    # Use PostgreSQL's INSERT ... ON CONFLICT to handle duplicates
    stmt = insert(StreamSubscription).values(subscription_data)

    # If subscription exists, update is_active to True
    stmt = stmt.on_conflict_do_update(
        constraint="uq_stream_sub_unique", set_={"is_active": True}
    )

    result = await db.execute(stmt)
    return result.rowcount or 0


async def seed_subscriptions(
    user_id: str, symbols: Iterable[str], book: str = "NASDAQ", active: bool = False
) -> None:
    syms = [s.upper() for s in symbols]

    async with AsyncSessionLocal() as db:
        # Bulk insert all subscription types
        added_ohlcv = await bulk_add_subscriptions(
            db, user_id, "ohlcv", syms, is_active=active
        )
        added_l1 = await bulk_add_subscriptions(
            db, user_id, "quotes", syms, is_active=active
        )
        added_l2 = await bulk_add_subscriptions(
            db, user_id, "level2", syms, book=book, is_active=active
        )

        # Single commit for all operations
        await db.commit()

    print(
        f"Seeded subscriptions for user {user_id}: OHLCV={added_ohlcv}, L1={added_l1}, L2[{book}]={added_l2}"
    )


async def main_async() -> None:
    parser = argparse.ArgumentParser(
        description="Subscribe a user to a set of symbols for OHLCV, L1, and L2"
    )
    parser.add_argument(
        "--user-id",
        required=False,
        default=env.OWNER_ID,
        help="User ID to seed subscriptions for (default: env.OWNER_ID)",
    )
    parser.add_argument(
        "--symbols",
        required=False,
        help="Comma-separated list of symbols to subscribe (default: 25 FAANG-like)",
    )
    parser.add_argument(
        "--book",
        required=False,
        choices=["NASDAQ", "NYSE"],
        default="NASDAQ",
        help="Order book for Level 2 subscriptions (default: NASDAQ)",
    )
    parser.add_argument(
        "--active",
        action="store_true",
        help="Create subscriptions as active immediately (default: inactive)",
    )
    args = parser.parse_args()

    # Clear existing subscriptions first
    await clear_subscriptions(args.user_id)

    symbols = _parse_symbols(args.symbols)
    await seed_subscriptions(args.user_id, symbols, book=args.book, active=args.active)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
