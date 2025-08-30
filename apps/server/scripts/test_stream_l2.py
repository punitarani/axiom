import argparse
import asyncio
import contextlib
from typing import List

from schwab.streaming import StreamClient

from axiom.env import env
from axiom.mdata import SchwabAuthService

# Default to env.OWNER_ID so you don't need to pass it via CLI each time.
DEFAULT_USER_ID = env.OWNER_ID


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test Schwab Level 2 streaming (NASDAQ or NYSE book)"
    )
    parser.add_argument(
        "--user-id",
        required=False,
        default=DEFAULT_USER_ID,
        help="Owner user ID to look up Schwab tokens for (defaults to DEFAULT_USER_ID)",
    )
    parser.add_argument(
        "--symbols",
        required=False,
        default="SPY",
        help="Comma-separated symbols to stream (default: SPY)",
    )
    parser.add_argument(
        "--book",
        required=False,
        choices=["NASDAQ", "NYSE"],
        default="NASDAQ",
        help="Order book to stream (default: NASDAQ)",
    )
    parser.add_argument(
        "--seconds",
        type=int,
        required=False,
        default=30,
        help="How long to keep the stream open before exiting (default: 30)",
    )
    args = parser.parse_args()

    user_id = args.user_id
    if not user_id or user_id == "<PUT_USER_ID_HERE>":
        print(
            "Please set DEFAULT_USER_ID in scripts/test_stream_l2.py or provide --user-id."
        )
        return

    symbols: List[str] = [
        s.strip().upper() for s in args.symbols.split(",") if s.strip()
    ]
    if not symbols:
        symbols = ["SPY"]

    auth = SchwabAuthService()
    client = await auth.get_client_for_user(user_id)
    if client is None:
        print("No Schwab client available for this user. Complete OAuth first.")
        return

    # Provide account_id to StreamClient for reliable login
    acct_resp = await client.get_account_numbers()
    acct_numbers = acct_resp.json() or []
    account_id = None
    if acct_numbers:
        try:
            account_id = int(
                (
                    acct_numbers[0].get("accountNumber")
                    or acct_numbers[0].get("account_number")
                ).strip()
            )
        except Exception:
            account_id = None

    stream = StreamClient(client, account_id=account_id)

    def on_book(msg):
        print(f"{args.book} L2 message:", msg)

    if args.book == "NYSE":
        stream.add_nyse_book_handler(on_book)
    else:
        stream.add_nasdaq_book_handler(on_book)

    # Open websocket session
    await stream.login()

    print(f"Subscribing to {args.book} L2 book for: {symbols} ...")
    if args.book == "NYSE":
        await stream.nyse_book_subs(symbols)
    else:
        await stream.nasdaq_book_subs(symbols)

    # Pump the websocket to receive messages
    async def _pump():
        while True:
            await stream.handle_message()

    task = asyncio.create_task(_pump())
    try:
        await asyncio.sleep(args.seconds)
    finally:
        print("Unsubscribing...")
        try:
            if args.book == "NYSE":
                await stream.nyse_book_unsubs(symbols)
            else:
                await stream.nasdaq_book_unsubs(symbols)
        except Exception:
            pass
        try:
            task.cancel()
            with contextlib.suppress(Exception):
                await task
        except Exception:
            pass
        try:
            await stream.logout()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
