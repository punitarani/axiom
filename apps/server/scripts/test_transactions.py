import argparse
import asyncio
import json
from datetime import date, datetime

from axiom.env import env
from axiom.mdata import SchwabAuthService

# Default to env.OWNER_ID so you don't need to pass it via CLI each time.
DEFAULT_USER_ID = env.OWNER_ID


def _parse_date(value: str):
    try:
        if len(value) == 10:
            return date.fromisoformat(value)
        return datetime.fromisoformat(value)
    except Exception:
        raise argparse.ArgumentTypeError(
            "Invalid date format. Use YYYY-MM-DD or ISO8601 datetime"
        )


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test Schwab transactions fetch (no persistence)"
    )
    parser.add_argument(
        "--user-id",
        required=False,
        default=DEFAULT_USER_ID,
        help="Owner user ID to look up Schwab tokens for (defaults to DEFAULT_USER_ID)",
    )
    parser.add_argument(
        "--account-hash",
        required=False,
        help="If provided, only fetch transactions for this account hash",
    )
    parser.add_argument(
        "--start-date",
        type=_parse_date,
        required=False,
        help="Only transactions after this date (YYYY-MM-DD or ISO8601). Optional",
    )
    parser.add_argument(
        "--end-date",
        type=_parse_date,
        required=False,
        help="Only transactions before this date (YYYY-MM-DD or ISO8601). Optional",
    )
    parser.add_argument(
        "--symbol",
        required=False,
        help="Filter by symbol (optional)",
    )
    parser.add_argument(
        "--types",
        required=False,
        help="Comma-separated transaction types (e.g., TRADE,DIVIDEND_OR_INTEREST). Optional",
    )
    args = parser.parse_args()

    user_id = args.user_id
    if not user_id or user_id == "<PUT_USER_ID_HERE>":
        print(
            "Please set DEFAULT_USER_ID in scripts/test_transactions.py or provide --user-id."
        )
        return

    auth = SchwabAuthService()
    client = await auth.get_client_for_user(user_id)
    if client is None:
        print("No Schwab client available for this user. Complete OAuth first.")
        return

    # Build mapping (accountNumber -> hash)
    print("Fetching account numbers...")
    resp = await client.get_account_numbers()
    print(f"status: {resp.status_code}")
    resp.raise_for_status()
    acct_numbers = resp.json() or []
    mappings = []
    for entry in acct_numbers or []:
        number = entry.get("accountNumber") or entry.get("account_number")
        acc_hash = entry.get("hashValue") or entry.get("hash")
        if number and acc_hash:
            mappings.append({"accountNumber": number, "hash": acc_hash})

    if not mappings:
        print("No account mappings available; cannot fetch transactions.")
        return

    print("\nAccount mappings (number -> hash):")
    print(json.dumps(mappings, indent=2))

    # Compose filters
    params: dict = {}
    if args.start_date:
        params["start_date"] = args.start_date
    if args.end_date:
        params["end_date"] = args.end_date
    if args.symbol:
        params["symbol"] = args.symbol
    if args.types:
        params["transaction_types"] = [
            t.strip().upper() for t in args.types.split(",") if t.strip()
        ]

    target_hashes = (
        [args.account_hash] if args.account_hash else [m["hash"] for m in mappings]
    )

    for acc_hash in target_hashes:
        print(f"\nFetching transactions for account hash: {acc_hash}...")
        r = await client.get_transactions(acc_hash, **params)
        print(f"status: {r.status_code}")
        r.raise_for_status()
        txns = r.json() or []
        print(f"count: {len(txns)}")
        print(json.dumps(txns, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
