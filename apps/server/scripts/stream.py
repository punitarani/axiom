import argparse
import asyncio
import contextlib
from typing import Dict, List, Tuple

from sqlalchemy import select, update

from axiom.db.client import AsyncSessionLocal
from axiom.db.models.subscription import StreamSubscription
from axiom.env import env
from axiom.mdata import MarketDataStreamingService


async def fetch_all_subscriptions(
    user_id: str,
) -> Tuple[List[str], Dict[str, List[str]], List[str]]:
    """
    Return ALL DB subscriptions for the user (regardless of is_active status):
      - quotes: list of symbols
      - level2: dict mapping book -> list of symbols
      - ohlcv: list of symbols
    """
    quotes: List[str] = []
    level2: Dict[str, List[str]] = {}
    ohlcv: List[str] = []

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(
                StreamSubscription.stream_type,
                StreamSubscription.symbol,
                StreamSubscription.book,
            ).where(StreamSubscription.user_id == user_id)
            # Remove is_active filter - get ALL subscriptions
        )
        for row in result.fetchall():
            stream_type, symbol, book = row
            symbol_up = (symbol or "").upper()
            if not symbol_up:
                continue
            if stream_type == "quotes":
                quotes.append(symbol_up)
            elif stream_type == "level2":
                key = (book or "NASDAQ").upper()
                level2.setdefault(key, []).append(symbol_up)
            elif stream_type == "ohlcv":
                ohlcv.append(symbol_up)

    # Deduplicate
    quotes = sorted(list(set(quotes)))
    for k in list(level2.keys()):
        level2[k] = sorted(list(set(level2[k])))
    ohlcv = sorted(list(set(ohlcv)))

    return quotes, level2, ohlcv


async def fetch_current_subscriptions(
    user_id: str,
) -> Tuple[List[str], Dict[str, List[str]], List[str]]:
    """
    Return current ACTIVE DB subscriptions for the user:
      - quotes: list of symbols
      - level2: dict mapping book -> list of symbols
      - ohlcv: list of symbols
    """
    quotes: List[str] = []
    level2: Dict[str, List[str]] = {}
    ohlcv: List[str] = []

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(
                StreamSubscription.stream_type,
                StreamSubscription.symbol,
                StreamSubscription.book,
            )
            .where(StreamSubscription.user_id == user_id)
            .where(StreamSubscription.is_active)
        )
        for row in result.fetchall():
            stream_type, symbol, book = row
            symbol_up = (symbol or "").upper()
            if not symbol_up:
                continue
            if stream_type == "quotes":
                quotes.append(symbol_up)
            elif stream_type == "level2":
                key = (book or "NASDAQ").upper()
                level2.setdefault(key, []).append(symbol_up)
            elif stream_type == "ohlcv":
                ohlcv.append(symbol_up)

    # Deduplicate
    quotes = sorted(list(set(quotes)))
    for k in list(level2.keys()):
        level2[k] = sorted(list(set(level2[k])))
    ohlcv = sorted(list(set(ohlcv)))

    return quotes, level2, ohlcv


async def activate_all_subscriptions(user_id: str) -> int:
    """Activate all subscriptions for a user when stream starts."""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import update

        result = await db.execute(
            update(StreamSubscription)
            .where(StreamSubscription.user_id == user_id)
            .values(is_active=True)
            .execution_options(synchronize_session=False)
        )
        await db.commit()
        count = result.rowcount or 0
        print(f"Activated {count} subscriptions for user {user_id}")
        return count


async def deactivate_all_subscriptions(user_id: str) -> int:
    """Deactivate all subscriptions for a user when stream ends."""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import update

        result = await db.execute(
            update(StreamSubscription)
            .where(StreamSubscription.user_id == user_id)
            .values(is_active=False)
            .execution_options(synchronize_session=False)
        )
        await db.commit()
        count = result.rowcount or 0
        print(f"Deactivated {count} subscriptions for user {user_id}")
        return count


async def diff_symbols(old: List[str], new: List[str]) -> Tuple[List[str], List[str]]:
    old_set = set([s.upper() for s in old])
    new_set = set([s.upper() for s in new])
    to_add = sorted(list(new_set - old_set))
    to_remove = sorted(list(old_set - new_set))
    return to_add, to_remove


async def set_active_for_symbols(
    user_id: str,
    stream_type: str,
    symbols: List[str],
    *,
    book: str | None = None,
    active: bool,
) -> int:
    if not symbols:
        return 0
    sym_upper = [s.upper() for s in symbols]
    async with AsyncSessionLocal() as db:
        where_clause = [
            StreamSubscription.user_id == user_id,
            StreamSubscription.stream_type == stream_type,
            StreamSubscription.symbol.in_(sym_upper),
        ]
        if book is not None:
            where_clause.append(StreamSubscription.book == book)
        result = await db.execute(
            update(StreamSubscription)
            .where(*where_clause)
            .values(is_active=active)
            .execution_options(synchronize_session=False)
        )
        await db.commit()
        return result.rowcount or 0


async def supervisor(
    user_id: str,
    poll_seconds: float,
    deactivate_on_exit: bool = False,
    resubscribe_full: bool = True,
) -> None:
    svc = MarketDataStreamingService()
    stop_event = asyncio.Event()

    # State we track to compute diffs
    current_quotes: List[str] = []
    current_level2: Dict[str, List[str]] = {}
    current_ohlcv: List[str] = []

    async def _graceful_shutdown():
        stop_event.set()
        await svc.stop()
        if deactivate_on_exit:
            # Mark all subscriptions for this user as inactive on shutdown
            await deactivate_all_subscriptions(user_id)

    # No-op signal handling placeholder removed; rely on cancellation

    # Initial login and subscriptions
    await svc.login(user_id)

    # Activate ALL subscriptions in the database first
    print("Activating all subscriptions...")
    await activate_all_subscriptions(user_id)

    # Now fetch all active subscriptions (should be all of them now)
    quotes, l2, ohlcv = await fetch_current_subscriptions(user_id)
    current_quotes = quotes
    current_level2 = l2
    current_ohlcv = ohlcv

    # Log what we found
    print(
        f"Found subscriptions: {len(quotes)} quotes, {sum(len(symbols) for symbols in l2.values())} level2, {len(ohlcv)} ohlcv"
    )

    # Start streams matching current DB state
    async with AsyncSessionLocal() as db:
        if current_quotes:
            print(
                f"Starting Level 1 streams for {len(current_quotes)} symbols: {current_quotes}"
            )
            await svc.start_level_one(db, user_id, current_quotes)
        for book, symbols in current_level2.items():
            if symbols:
                print(
                    f"Starting Level 2 streams for {len(symbols)} symbols on {book}: {symbols}"
                )
                await svc.start_level_two(db, user_id, symbols, book=book)
        if current_ohlcv:
            print(
                f"Starting chart streams for {len(current_ohlcv)} symbols: {current_ohlcv}"
            )
            await svc.start_charts(db, user_id, current_ohlcv)

    # Start the message pump
    pump_task = asyncio.create_task(svc.pump_messages_forever(stop_event))

    try:
        # Poll for subscription changes
        while not stop_event.is_set():
            try:
                await asyncio.sleep(poll_seconds)
            except asyncio.CancelledError:
                print("Supervisor loop cancelled, initiating cleanup...")
                break

            # Log stream health periodically
            if hasattr(svc, "get_message_stats"):
                stats = svc.get_message_stats()

                # Format basic stats
                msg_count = stats.get("total_messages", 0)
                seconds_since_last = stats.get("seconds_since_last_message")
                connected = stats.get("is_connected", False)

                print(
                    f"Stream: {msg_count} messages, connected: {connected}, last message: {seconds_since_last:.1f}s ago"
                    if seconds_since_last
                    else f"Stream: {msg_count} messages, connected: {connected}"
                )

                # Format batcher stats
                for batcher_type in ["l1", "l2", "chart"]:
                    batcher_key = f"{batcher_type}_batcher"
                    if batcher_key in stats:
                        batcher = stats[batcher_key]
                        queue_size = batcher.get("queue_size", 0)
                        total_flushes = batcher.get("total_flushes", 0)
                        total_items = batcher.get("total_items_flushed", 0)
                        failed_flushes = batcher.get("failed_flushes", 0)
                        since_last_flush = batcher.get("seconds_since_last_flush")
                        running = batcher.get("is_running", False)

                        status = f"{batcher_type.upper()}: queue={queue_size}, flushes={total_flushes}, items={total_items}, failures={failed_flushes}, running={running}"
                        if since_last_flush is not None:
                            status += f", last_flush={since_last_flush:.1f}s_ago"
                        print(f"  {status}")

                # Check for stale connection
                if seconds_since_last and seconds_since_last > 300:  # 5 minutes
                    print(
                        f"WARNING: No messages received for {seconds_since_last:.1f} seconds"
                    )

                # Check for stale batchers
                for batcher_type in ["l1", "l2", "chart"]:
                    batcher_key = f"{batcher_type}_batcher"
                    if batcher_key in stats:
                        batcher = stats[batcher_key]
                        since_last_flush = batcher.get("seconds_since_last_flush")
                        expected_interval = (
                            10.0 if batcher_type in ["l1", "l2"] else 30.0
                        )
                        if (
                            since_last_flush
                            and since_last_flush > expected_interval * 2
                        ):
                            print(
                                f"WARNING: {batcher_type.upper()} batcher hasn't flushed in {since_last_flush:.1f}s (expected every {expected_interval}s)"
                            )

            new_quotes, new_level2, new_ohlcv = await fetch_current_subscriptions(
                user_id
            )

            # Level 1 diffs
            add_q, rem_q = await diff_symbols(current_quotes, new_quotes)
            if add_q or rem_q:
                print(f"Level 1 changes: +{add_q} -{rem_q}")
                if resubscribe_full:
                    await svc.set_level_one_stream(user_id, new_quotes)
                    # Reflect DB state
                    if add_q:
                        await set_active_for_symbols(
                            user_id, "quotes", add_q, active=True
                        )
                    if rem_q:
                        await set_active_for_symbols(
                            user_id, "quotes", rem_q, active=False
                        )
                else:
                    async with AsyncSessionLocal() as db:
                        if add_q:
                            await svc.add_symbols(db, user_id, "quotes", add_q)
                        if rem_q:
                            await svc.remove_symbols(db, user_id, "quotes", rem_q)
                current_quotes = new_quotes

            # Level 2 diffs per book
            all_books = set(list(current_level2.keys()) + list(new_level2.keys()))
            for book in sorted(all_books):
                old_list = current_level2.get(book, [])
                new_list = new_level2.get(book, [])
                add_l2, rem_l2 = await diff_symbols(old_list, new_list)
                if add_l2 or rem_l2:
                    print(f"Level 2 {book} changes: +{add_l2} -{rem_l2}")
                    if resubscribe_full:
                        await svc.set_level_two_stream(user_id, new_list, book=book)
                        # Reflect DB state
                        if add_l2:
                            await set_active_for_symbols(
                                user_id, "level2", add_l2, book=book, active=True
                            )
                        if rem_l2:
                            await set_active_for_symbols(
                                user_id, "level2", rem_l2, book=book, active=False
                            )
                    else:
                        async with AsyncSessionLocal() as db:
                            if add_l2:
                                await svc.add_symbols(
                                    db, user_id, "level2", add_l2, book=book
                                )
                            if rem_l2:
                                await svc.remove_symbols(
                                    db, user_id, "level2", rem_l2, book=book
                                )
                current_level2[book] = new_list
            # Remove books that no longer exist
            for book in list(current_level2.keys()):
                if book not in new_level2:
                    current_level2.pop(book, None)

            # OHLCV/Chart changes
            add_ohlcv, rem_ohlcv = await diff_symbols(current_ohlcv, new_ohlcv)
            if add_ohlcv or rem_ohlcv:
                print(f"Chart changes: +{add_ohlcv} -{rem_ohlcv}")
                if resubscribe_full:
                    await svc.set_chart_stream(user_id, new_ohlcv)
                    # Reflect DB state
                    if add_ohlcv:
                        await set_active_for_symbols(
                            user_id, "ohlcv", add_ohlcv, active=True
                        )
                    if rem_ohlcv:
                        await set_active_for_symbols(
                            user_id, "ohlcv", rem_ohlcv, active=False
                        )
                else:
                    async with AsyncSessionLocal() as db:
                        if add_ohlcv:
                            await svc.add_symbols(db, user_id, "ohlcv", add_ohlcv)
                        if rem_ohlcv:
                            await svc.remove_symbols(db, user_id, "ohlcv", rem_ohlcv)
            current_ohlcv = new_ohlcv
    except asyncio.CancelledError:
        pass
    finally:
        with contextlib.suppress(Exception):
            pump_task.cancel()
            await pump_task
        await _graceful_shutdown()


async def main_async() -> None:
    parser = argparse.ArgumentParser(description="Run market data streams supervisor")
    parser.add_argument(
        "--user-id",
        required=False,
        default=env.OWNER_ID,
        help="User ID whose Schwab tokens and subscriptions to use (default: env.OWNER_ID)",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=5.0,
        help="Polling interval for subscription changes",
    )
    parser.add_argument(
        "--deactivate-on-exit",
        action="store_true",
        help="On shutdown, mark the user's subscriptions inactive",
    )
    parser.add_argument(
        "--no-resubscribe-full",
        action="store_true",
        help="Disable full resubscribe optimization; use incremental add/remove",
    )
    args = parser.parse_args()

    await supervisor(
        args.user_id,
        args.poll_seconds,
        deactivate_on_exit=args.deactivate_on_exit,
        resubscribe_full=(not args.no_resubscribe_full),
    )


def main() -> None:
    import signal
    import sys

    async def run_with_cleanup():
        # Set up signal handlers for graceful shutdown
        shutdown_event = asyncio.Event()

        def signal_handler(sig, _frame):
            print(f"\nReceived signal {sig}, initiating graceful shutdown...")
            shutdown_event.set()

        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

        try:
            # Create task for main_async
            main_task = asyncio.create_task(main_async())

            # Wait for either completion or shutdown signal
            _done, pending = await asyncio.wait(
                [main_task, asyncio.create_task(shutdown_event.wait())],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # If shutdown was requested, cancel main task
            if shutdown_event.is_set():
                print("Graceful shutdown initiated...")
                main_task.cancel()
                try:
                    await main_task
                except asyncio.CancelledError:
                    print("Main task cancelled successfully")
            else:
                # Main task completed normally
                await main_task

            # Cancel any remaining tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        except Exception as e:
            print(f"Error during execution: {e}")
            sys.exit(1)
        finally:
            print("Cleanup complete")

    asyncio.run(run_with_cleanup())


if __name__ == "__main__":
    main()
