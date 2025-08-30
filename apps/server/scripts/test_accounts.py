import argparse
import asyncio
import json

from axiom.env import env
from axiom.mdata import SchwabAuthService

# Default to env.OWNER_ID so you don't need to pass it via CLI each time.
DEFAULT_USER_ID = env.OWNER_ID


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test Schwab account fetch (no persistence)"
    )
    parser.add_argument(
        "--user-id",
        required=False,
        default=DEFAULT_USER_ID,
        help="Owner user ID to look up Schwab tokens for (defaults to DEFAULT_USER_ID)",
    )
    args = parser.parse_args()

    user_id = args.user_id
    if not user_id or user_id == "<PUT_USER_ID_HERE>":
        print(
            "Please set DEFAULT_USER_ID in scripts/test_accounts.py or provide --user-id."
        )
        return

    auth = SchwabAuthService()
    client = await auth.get_client_for_user(user_id)
    if client is None:
        print("No Schwab client available for this user. Complete OAuth first.")
        return

    # Fetch account numbers (maps account numbers to hashes)
    print("Fetching account numbers...")
    resp = await client.get_account_numbers()
    print(f"status: {resp.status_code}")
    resp.raise_for_status()
    acct_numbers = resp.json()
    print(json.dumps(acct_numbers, indent=2))

    # Fetch all accounts
    print("\nFetching accounts...")
    resp2 = await client.get_accounts()
    print(f"status: {resp2.status_code}")
    resp2.raise_for_status()
    accounts = resp2.json()
    print(json.dumps(accounts, indent=2))

    # Build mapping (accountNumber -> hash) and fetch details for each account
    mappings = []
    for entry in acct_numbers or []:
        number = entry.get("accountNumber") or entry.get("account_number")
        acc_hash = entry.get("hashValue") or entry.get("hash")
        if number and acc_hash:
            mappings.append({"accountNumber": number, "hash": acc_hash})

    if mappings:
        print("\nAccount mappings (number -> hash):")
        print(json.dumps(mappings, indent=2))

        for m in mappings:
            acc_hash = m["hash"]
            print(f"\nFetching details for account hash: {acc_hash}...")
            resp3 = await client.get_account(acc_hash)
            print(f"status: {resp3.status_code}")
            resp3.raise_for_status()
            detail = resp3.json()
            # Print a compact summary plus the full payload
            try:
                sa = detail.get("securitiesAccount", {})
                summary = {
                    "accountNumber": sa.get("accountNumber"),
                    "type": sa.get("type"),
                    "equity": sa.get("currentBalances", {}).get("equity"),
                    "buyingPower": sa.get("currentBalances", {}).get("buyingPower"),
                }
                print("Summary:", json.dumps(summary, indent=2))
            except Exception:
                pass
            print(json.dumps(detail, indent=2))
    else:
        print("No account mappings available; cannot fetch account details.")


if __name__ == "__main__":
    asyncio.run(main())
