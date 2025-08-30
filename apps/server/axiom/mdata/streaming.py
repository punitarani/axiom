from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from axiom.db.client import AsyncSessionLocal
from axiom.db.models import (
    Chart,
    InstrumentType,
    LevelOne,
    LevelTwo,
    OrderSide,
    Security,
)
from axiom.db.models.enums import Timeframe
from axiom.lib.beque import Beque
from axiom.mdata.auth import SchwabAuthService
from axiom.mdata.subscriptions import SubscriptionService


class MarketDataStreamingService:
    def __init__(self, auth: Optional[SchwabAuthService] = None):
        import logging

        self.logger = logging.getLogger(__name__)
        self.auth = auth or SchwabAuthService()
        self.subscription_service = SubscriptionService()
        self._stream = None
        self._lock = asyncio.Lock()
        self._l1_batcher: Optional[Beque[dict]] = None
        self._l2_batcher: Optional[Beque[dict]] = None
        self._chart_batcher: Optional[Beque[dict]] = None
        self._security_cache: dict[str, Optional[Any]] = {}
        self._message_count = 0
        self._last_message_time = None
        # Store connection state for reconnection
        self._current_user_id: Optional[str] = None
        self._active_subscriptions: dict = {
            "l1_symbols": [],
            "l2_symbols": [],
            "l2_book": "NASDAQ",
            "chart_symbols": [],
        }

    async def _ensure_stream(self, user_id: str):
        async with self._lock:
            if self._stream is not None:
                return self._stream
            client = await self.auth.get_client_for_user(user_id)
            if client is None:
                raise RuntimeError("No Schwab client for user")
            from schwab.streaming import StreamClient

            # Provide account_id to StreamClient for reliable login
            account_id = None
            try:
                acct_resp = await client.get_account_numbers()
                acct_numbers = acct_resp.json() or []
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
            except Exception:
                account_id = None

            self._stream = StreamClient(client, account_id=account_id)
            return self._stream

    async def login(self, user_id: str) -> None:
        self.logger.info(f"Logging in stream for user {user_id}")
        stream = await self._ensure_stream(user_id)
        await stream.login()
        self.logger.info(f"Stream login successful for user {user_id}")

    async def logout(self) -> None:
        if self._stream is not None:
            try:
                await self._stream.logout()
            except Exception:
                pass

    async def _reconnect(self) -> None:
        """Reconnect to streaming service and restore subscriptions."""
        if not self._current_user_id:
            raise RuntimeError("No user_id stored for reconnection")

        self.logger.info("Reconnecting to streaming service...")

        # Clear the old stream
        self._stream = None

        # Re-establish connection
        await self.login(self._current_user_id)

        # Restore subscriptions
        if self._active_subscriptions["l1_symbols"]:
            self.logger.info(
                f"Restoring L1 subscriptions: {len(self._active_subscriptions['l1_symbols'])} symbols"
            )
            await self._stream.level_one_equity_subs(
                self._active_subscriptions["l1_symbols"]
            )

        if self._active_subscriptions["l2_symbols"]:
            self.logger.info(
                f"Restoring L2 subscriptions: {len(self._active_subscriptions['l2_symbols'])} symbols"
            )
            book = self._active_subscriptions["l2_book"]
            if book.upper() == "NYSE":
                await self._stream.nyse_book_subs(
                    self._active_subscriptions["l2_symbols"]
                )
            else:
                await self._stream.nasdaq_book_subs(
                    self._active_subscriptions["l2_symbols"]
                )

        if self._active_subscriptions["chart_symbols"]:
            self.logger.info(
                f"Restoring chart subscriptions: {len(self._active_subscriptions['chart_symbols'])} symbols"
            )
            await self._stream.chart_equity_subs(
                self._active_subscriptions["chart_symbols"]
            )

        self.logger.info("Subscription restoration complete")

    async def start_quotes(
        self, db: AsyncSession, user_id: str, symbols: Optional[Iterable[str]] = None
    ) -> None:
        await self._ensure_batchers()
        stream = await self._ensure_stream(user_id)
        if symbols is None:
            symbols = await self.subscription_service.list_symbols(
                db, user_id, stream_type="quotes"
            )
        symbols_list = list(symbols)

        # Store for reconnection
        self._current_user_id = user_id
        self._active_subscriptions["l1_symbols"] = symbols_list

        self.logger.info(
            f"Starting level 1 quotes for {len(symbols_list)} symbols: {symbols_list}"
        )
        await stream.level_one_equity_subs(symbols_list)

        def handler(msg):
            from datetime import datetime, timezone

            self._message_count += 1
            self._last_message_time = datetime.now(timezone.utc)

            if self._message_count % 100 == 0:  # Log every 100th message
                self.logger.info(f"Processed {self._message_count} L1 messages")

            entities = self._extract_l1_entities(msg)
            if not entities:
                if self._message_count % 10 == 0:  # Log empty messages occasionally
                    self.logger.warning(f"Received L1 message with no entities: {msg}")
                return

            self.logger.debug(f"L1 handler processing {len(entities)} entities")
            # Use background task with proper error handling
            asyncio.create_task(self._enqueue_l1_batch(entities))

        stream.add_level_one_equity_handler(handler)
        self.logger.info(f"Level 1 handler registered for {len(symbols_list)} symbols")

    async def start_level_one(
        self, db: AsyncSession, user_id: str, symbols: Optional[Iterable[str]] = None
    ) -> None:
        # Alias for clarity; quotes == L1 in schwab naming
        await self.start_quotes(db, user_id, symbols)

    async def start_level_two(
        self,
        db: AsyncSession,
        user_id: str,
        symbols: Optional[Iterable[str]] = None,
        book: str = "NASDAQ",
    ) -> None:
        await self._ensure_batchers()
        stream = await self._ensure_stream(user_id)
        if symbols is None:
            symbols = await self.subscription_service.list_symbols(
                db, user_id, stream_type="level2", book=book
            )

        symbols_list = list(symbols)

        # Store for reconnection
        self._current_user_id = user_id
        self._active_subscriptions["l2_symbols"] = symbols_list
        self._active_subscriptions["l2_book"] = book

        self.logger.info(
            f"Starting level 2 quotes for {len(symbols_list)} symbols on {book}: {symbols_list}"
        )

        if book.upper() == "NYSE":
            await stream.nyse_book_subs(symbols_list)
        else:
            await stream.nasdaq_book_subs(symbols_list)

        def handler(msg):
            from datetime import datetime, timezone

            self._message_count += 1
            self._last_message_time = datetime.now(timezone.utc)

            entities = self._extract_l2_entities(msg)
            if not entities:
                if self._message_count % 10 == 0:  # Log empty messages occasionally
                    self.logger.warning(f"Received L2 message with no entities: {msg}")
                return

            self.logger.debug(
                f"L2 handler processing {len(entities)} entities for {book}"
            )
            # Use background task with proper error handling
            asyncio.create_task(self._enqueue_l2_batch(entities))

        if book.upper() == "NYSE":
            stream.add_nyse_book_handler(handler)
        else:
            stream.add_nasdaq_book_handler(handler)

        self.logger.info(
            f"Level 2 handler registered for {len(symbols_list)} symbols on {book}"
        )

    async def start_charts(
        self, db: AsyncSession, user_id: str, symbols: Optional[Iterable[str]] = None
    ) -> None:
        await self._ensure_batchers()
        stream = await self._ensure_stream(user_id)
        if symbols is None:
            symbols = await self.subscription_service.list_symbols(
                db, user_id, stream_type="ohlcv"
            )
        symbols_list = list(symbols)

        # Store for reconnection
        self._current_user_id = user_id
        self._active_subscriptions["chart_symbols"] = symbols_list

        self.logger.info(
            f"Starting chart streams for {len(symbols_list)} symbols: {symbols_list}"
        )
        await stream.chart_equity_subs(symbols_list)

        def handler(msg):
            from datetime import datetime, timezone

            self._message_count += 1
            self._last_message_time = datetime.now(timezone.utc)

            if self._message_count % 100 == 0:  # Log every 100th message
                self.logger.info(f"Processed {self._message_count} chart messages")

            entities = self._extract_chart_entities(msg)
            if not entities:
                if self._message_count % 10 == 0:  # Log empty messages occasionally
                    self.logger.warning(
                        f"Received chart message with no entities: {msg}"
                    )
                return

            self.logger.debug(f"Chart handler processing {len(entities)} entities")
            # Use background task with proper error handling
            asyncio.create_task(self._enqueue_chart_batch(entities))

        stream.add_chart_equity_handler(handler)
        self.logger.info(f"Chart handler registered for {len(symbols_list)} symbols")

    async def add_symbols(
        self,
        db: AsyncSession,
        user_id: str,
        stream_type: str,
        symbols: Iterable[str],
        book: Optional[str] = None,
    ) -> None:
        await self.subscription_service.add_symbols(
            db, user_id, stream_type, symbols, book
        )
        stream = await self._ensure_stream(user_id)
        if stream_type == "quotes":
            await stream.level_one_equity_add(list(symbols))
        elif stream_type == "level2":
            if (book or "NASDAQ").upper() == "NYSE":
                await stream.nyse_book_add(list(symbols))
            else:
                await stream.nasdaq_book_add(list(symbols))
        elif stream_type == "ohlcv":
            await stream.chart_equity_add(list(symbols))

    async def remove_symbols(
        self,
        db: AsyncSession,
        user_id: str,
        stream_type: str,
        symbols: Iterable[str],
        book: Optional[str] = None,
    ) -> None:
        await self.subscription_service.remove_symbols(
            db, user_id, stream_type, symbols, book
        )
        stream = await self._ensure_stream(user_id)
        if stream_type == "quotes":
            await stream.level_one_equity_unsubs(list(symbols))
        elif stream_type == "level2":
            if (book or "NASDAQ").upper() == "NYSE":
                await stream.nyse_book_unsubs(list(symbols))
            else:
                await stream.nasdaq_book_unsubs(list(symbols))
        elif stream_type == "ohlcv":
            await stream.chart_equity_unsubs(list(symbols))

    async def set_level_one_stream(self, user_id: str, symbols: Iterable[str]) -> None:
        """Replace the Level 1 subscription set on the wire without touching DB."""
        stream = await self._ensure_stream(user_id)
        await stream.level_one_equity_subs(list(symbols))

    async def set_level_two_stream(
        self, user_id: str, symbols: Iterable[str], *, book: str = "NASDAQ"
    ) -> None:
        """Replace the Level 2 subscription set for a book on the wire without touching DB."""
        stream = await self._ensure_stream(user_id)
        if (book or "NASDAQ").upper() == "NYSE":
            await stream.nyse_book_subs(list(symbols))
        else:
            await stream.nasdaq_book_subs(list(symbols))

    async def set_chart_stream(self, user_id: str, symbols: Iterable[str]) -> None:
        """Replace the chart subscription set on the wire without touching DB."""
        stream = await self._ensure_stream(user_id)
        await stream.chart_equity_subs(list(symbols))

    async def pump_messages_forever(self, stop_event: asyncio.Event) -> None:
        from datetime import datetime, timezone

        if self._stream is None:
            self.logger.warning("Stream is None, cannot pump messages")
            return

        consecutive_errors = 0
        max_consecutive_errors = 10
        last_health_check = datetime.now(timezone.utc)
        health_check_interval = 60  # seconds

        self.logger.info("Starting message pump")

        while not stop_event.is_set():
            try:
                await self._stream.handle_message()
                consecutive_errors = 0  # Reset on successful message

                # Periodic health check logging
                now = datetime.now(timezone.utc)
                if (now - last_health_check).total_seconds() >= health_check_interval:
                    last_msg_age = (
                        (now - self._last_message_time).total_seconds()
                        if self._last_message_time
                        else "unknown"
                    )
                    self.logger.info(
                        f"Stream health: {self._message_count} total messages, last message {last_msg_age}s ago"
                    )
                    last_health_check = now

                    # Warn if no messages received in a while
                    if (
                        self._last_message_time
                        and isinstance(last_msg_age, (int, float))
                        and last_msg_age > 300
                    ):  # 5 minutes
                        self.logger.warning(
                            f"No messages received for {last_msg_age:.1f} seconds - connection may be stale"
                        )

            except asyncio.CancelledError:
                self.logger.info("Message pump cancelled")
                break
            except Exception as e:
                # Handle WebSocket connection closures separately from other errors
                from websockets.exceptions import ConnectionClosed, ConnectionClosedOK

                if isinstance(e, (ConnectionClosed, ConnectionClosedOK)):
                    self.logger.info(
                        f"WebSocket connection closed: {type(e).__name__}: {e}"
                    )

                    # Check if it's likely outside market hours
                    now = datetime.now(timezone.utc)
                    is_weekend = now.weekday() >= 5  # Saturday = 5, Sunday = 6

                    if is_weekend:
                        self.logger.info(
                            "Connection closed during weekend - this is normal (no market data)"
                        )
                        # On weekends, don't retry as frequently to avoid spam
                        if consecutive_errors >= 3:
                            self.logger.info(
                                "Multiple weekend connection closures - reducing retry frequency"
                            )
                            # Sleep longer between retries on weekends
                            await asyncio.sleep(min(30.0, 5.0 * consecutive_errors))
                    else:
                        self.logger.info(
                            "Connection closed during weekday - may be outside market hours or server maintenance"
                        )

                    # Only attempt reconnection if we haven't exceeded reasonable retry limits
                    if (
                        consecutive_errors < 5
                    ):  # Reduced from 10 to 5 for connection closures
                        self.logger.info(
                            f"Attempting to reconnect... (attempt {consecutive_errors + 1}/5)"
                        )

                        try:
                            await self._reconnect()
                            self.logger.info("Reconnection successful")
                            consecutive_errors = (
                                0  # Reset error count on successful reconnection
                            )
                            continue
                        except Exception as reconnect_error:
                            self.logger.error(f"Reconnection failed: {reconnect_error}")
                            consecutive_errors += 1
                    else:
                        self.logger.warning(
                            "Too many connection closure retries - will stop attempting reconnection"
                        )
                        consecutive_errors += 1
                else:
                    consecutive_errors += 1
                    self.logger.error(
                        f"Stream message error #{consecutive_errors}: {type(e).__name__}: {e}"
                    )

                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error(
                        f"Too many consecutive errors ({consecutive_errors}), stopping message pump"
                    )
                    break

                # Exponential backoff for retries
                sleep_time = min(0.1 * (2**consecutive_errors), 30.0)
                self.logger.info(f"Sleeping {sleep_time:.1f}s before retry")
                await asyncio.sleep(sleep_time)

        self.logger.info(
            f"Message pump stopped. Total messages processed: {self._message_count}"
        )

    async def stop(self) -> None:
        """Gracefully stop the streaming service and flush all pending data."""
        self.logger.info("Stopping streaming service...")

        # Stop batchers and ensure all data is flushed
        batchers = [
            ("L1", self._l1_batcher),
            ("L2", self._l2_batcher),
            ("Chart", self._chart_batcher),
        ]

        for name, batcher in batchers:
            if batcher is not None:
                try:
                    self.logger.info(f"Stopping {name} batcher...")
                    await batcher.stop()
                    self.logger.info(f"{name} batcher stopped and flushed")
                except Exception as e:
                    self.logger.error(f"Error stopping {name} batcher: {e}")

        # Clear batcher references
        self._l1_batcher = None
        self._l2_batcher = None
        self._chart_batcher = None

        # Logout stream
        try:
            await self.logout()
            self.logger.info("Stream logged out successfully")
        except Exception as e:
            self.logger.error(f"Error during stream logout: {e}")

        self._stream = None
        self.logger.info("Streaming service stopped")

    def get_stream(self):
        return self._stream

    def get_message_stats(self) -> Dict[str, Any]:
        """Get statistics about message processing for diagnostics."""
        from datetime import datetime, timezone

        stats = {
            "total_messages": self._message_count,
            "last_message_time": (
                self._last_message_time.isoformat() if self._last_message_time else None
            ),
            "is_connected": self._stream is not None,
        }
        if self._last_message_time:
            stats["seconds_since_last_message"] = (
                datetime.now(timezone.utc) - self._last_message_time
            ).total_seconds()

        # Add batcher health information
        for name, batcher in [
            ("l1", self._l1_batcher),
            ("l2", self._l2_batcher),
            ("chart", self._chart_batcher),
        ]:
            if batcher:
                stats[f"{name}_batcher"] = batcher.stats

        return stats

    async def _ensure_batchers(self) -> None:
        if self._l1_batcher is None:
            self._l1_batcher = Beque(
                max_batch_size=100,
                flush_interval=10.0,
                on_flush=self._flush_level_one,
                name="L1_Batcher",
            )
            await self._l1_batcher.start()
        if self._l2_batcher is None:
            self._l2_batcher = Beque(
                max_batch_size=100,
                flush_interval=10.0,
                on_flush=self._flush_level_two,
                name="L2_Batcher",
            )
            await self._l2_batcher.start()
        if self._chart_batcher is None:
            self._chart_batcher = Beque(
                max_batch_size=50,  # Charts might be larger/less frequent
                flush_interval=30.0,  # Charts can be batched longer
                on_flush=self._flush_charts,
                name="Chart_Batcher",
            )
            await self._chart_batcher.start()

    # ---------- Parsing helpers ----------
    def _extract_l1_entities(self, msg: Any) -> List[Dict[str, Any]]:
        content = []
        if isinstance(msg, dict) and msg.get("content"):
            raw = msg.get("content")
            content = raw if isinstance(raw, list) else [raw]
        elif isinstance(msg, list):
            content = msg
        elif isinstance(msg, dict):
            content = [msg]

        entities: List[Dict[str, Any]] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            symbol = (
                item.get("symbol")
                or item.get("SYMBOL")
                or item.get("key")
                or item.get("KEY")
            )
            if not symbol:
                continue

            def _num(*keys: str) -> Optional[float]:
                for k in keys:
                    v = item.get(k)
                    if v is not None:
                        try:
                            return float(v)
                        except Exception:
                            return None
                return None

            ent = {
                "symbol": str(symbol).upper(),
                "bid_price": _num("bidPrice", "BID_PRICE", "BID"),
                "ask_price": _num("askPrice", "ASK_PRICE", "ASK"),
                "last_price": _num("lastPrice", "LAST_PRICE", "LAST"),
                "bid_size": _num("bidSize", "BID_SIZE"),
                "ask_size": _num("askSize", "ASK_SIZE"),
                "last_size": _num("lastSize", "LAST_SIZE"),
                "mark_price": _num("mark", "MARK", "MARK_PRICE"),
                "daily_high": _num("highPrice", "HIGH_PRICE", "HIGH"),
                "daily_low": _num("lowPrice", "LOW_PRICE", "LOW"),
                "daily_open": _num("openPrice", "OPEN_PRICE", "OPEN"),
                "prev_close": _num("closePrice", "PREV_CLOSE", "CLOSE"),
                "daily_volume": _num("totalVolume", "VOLUME", "TOTAL_VOLUME"),
                "quote_time": item.get("quoteTime", item.get("QUOTE_TIME")),
                "trade_time": item.get("tradeTime", item.get("TRADE_TIME")),
                "is_realtime": bool(
                    item.get("isRealtime", item.get("IS_REAL_TIME", True))
                ),
            }
            entities.append(ent)
        return entities

    def _extract_l2_entities(self, msg: Any) -> List[Dict[str, Any]]:
        content = []
        if isinstance(msg, dict) and msg.get("content"):
            raw = msg.get("content")
            content = raw if isinstance(raw, list) else [raw]
        elif isinstance(msg, list):
            content = msg
        elif isinstance(msg, dict):
            content = [msg]

        entities: List[Dict[str, Any]] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            symbol = (
                item.get("symbol")
                or item.get("SYMBOL")
                or item.get("key")
                or item.get("KEY")
            )
            if not symbol:
                continue
            side_raw = (item.get("side") or item.get("SIDE") or "").upper()
            side = side_raw if side_raw in ("BID", "ASK") else None

            # Price level and size can appear in various keys
            def _num(*keys: str) -> Optional[float]:
                for k in keys:
                    v = item.get(k)
                    if v is not None:
                        try:
                            return float(v)
                        except Exception:
                            return None
                return None

            ent = {
                "symbol": str(symbol).upper(),
                "side": side,
                "price_level": _num("price", "PRICE", "priceLevel", "PRICE_LEVEL"),
                "size": _num("size", "SIZE"),
                "order_count": int(_num("orderCount", "ORDER_COUNT") or 0),
                "level_index": int(_num("levelIndex", "LEVEL_INDEX") or 0),
                "market_maker_id": item.get("marketMaker", item.get("MMID")),
                "mic_id": item.get("micId", item.get("MIC")),
                "quote_time": item.get("quoteTime", item.get("QUOTE_TIME")),
            }
            entities.append(ent)
        return entities

    def _extract_chart_entities(self, msg: Any) -> List[Dict[str, Any]]:
        content = []
        if isinstance(msg, dict) and msg.get("content"):
            raw = msg.get("content")
            content = raw if isinstance(raw, list) else [raw]
        elif isinstance(msg, list):
            content = msg
        elif isinstance(msg, dict):
            content = [msg]

        entities: List[Dict[str, Any]] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            symbol = (
                item.get("symbol")
                or item.get("SYMBOL")
                or item.get("key")
                or item.get("KEY")
            )
            if not symbol:
                continue

            def _num(*keys: str) -> Optional[float]:
                for k in keys:
                    v = item.get(k)
                    if v is not None:
                        try:
                            return float(v)
                        except Exception:
                            return None
                return None

            # Chart data often comes with OHLCV fields
            ent = {
                "symbol": str(symbol).upper(),
                "open_price": _num("openPrice", "OPEN_PRICE", "OPEN", "open"),
                "high_price": _num("highPrice", "HIGH_PRICE", "HIGH", "high"),
                "low_price": _num("lowPrice", "LOW_PRICE", "LOW", "low"),
                "close_price": _num("closePrice", "CLOSE_PRICE", "CLOSE", "close"),
                "volume": _num("volume", "VOLUME", "totalVolume", "TOTAL_VOLUME"),
                "trade_count": _num("tradeCount", "TRADE_COUNT"),
                "vwap": _num("vwap", "VWAP"),
                "timestamp": item.get("timestamp", item.get("TIMESTAMP")),
                "timeframe": item.get("timeframe", item.get("TIMEFRAME", "1MIN")),
            }
            entities.append(ent)
        return entities

    # ---------- Flush consumers ----------
    async def _flush_level_one(self, batch: List[Dict[str, Any]]) -> None:
        if not batch:
            return

        self.logger.info(f"Flushing L1 batch with {len(batch)} items")

        # Resolve symbols to security IDs in bulk
        symbols = sorted({b["symbol"] for b in batch if b.get("symbol")})
        async with AsyncSessionLocal() as db:
            symbol_to_id = await self._resolve_security_ids(db, symbols)
            missing_symbols = [s for s in symbols if not symbol_to_id.get(s)]
            if missing_symbols:
                self.logger.warning(
                    f"Missing security IDs for symbols: {missing_symbols}"
                )

            objs: List[LevelOne] = []
            now = datetime.now(timezone.utc)
            for b in batch:
                sec_id = symbol_to_id.get(b.get("symbol"))
                if not sec_id:
                    continue
                obj = LevelOne(
                    security_id=sec_id,
                    timestamp=now,
                    instrument_type=InstrumentType.EQUITY,
                    bid_price=self._to_price_int(b.get("bid_price")),
                    bid_size=self._to_int(b.get("bid_size")),
                    ask_price=self._to_price_int(b.get("ask_price")),
                    ask_size=self._to_int(b.get("ask_size")),
                    last_price=self._to_price_int(b.get("last_price")),
                    last_size=self._to_int(b.get("last_size")),
                    mark_price=self._to_price_int(b.get("mark_price")),
                    daily_high=self._to_price_int(b.get("daily_high")),
                    daily_low=self._to_price_int(b.get("daily_low")),
                    daily_open=self._to_price_int(b.get("daily_open")),
                    prev_close=self._to_price_int(b.get("prev_close")),
                    daily_volume=self._to_int(b.get("daily_volume")),
                    quote_time=self._to_int(b.get("quote_time")),
                    trade_time=self._to_int(b.get("trade_time")),
                    is_realtime=bool(b.get("is_realtime", True)),
                )
                objs.append(obj)

            if objs:
                self.logger.info(f"Saving {len(objs)} L1 records to database")
                db.add_all(objs)
                await db.commit()
                self.logger.debug("L1 batch commit successful")
            else:
                self.logger.warning(
                    f"No valid L1 objects created from batch of {len(batch)} items"
                )

    async def _flush_level_two(self, batch: List[Dict[str, Any]]) -> None:
        if not batch:
            return

        self.logger.info(f"Flushing L2 batch with {len(batch)} items")

        symbols = sorted({b["symbol"] for b in batch if b.get("symbol")})
        async with AsyncSessionLocal() as db:
            symbol_to_id = await self._resolve_security_ids(db, symbols)
            missing_symbols = [s for s in symbols if not symbol_to_id.get(s)]
            if missing_symbols:
                self.logger.warning(
                    f"Missing security IDs for L2 symbols: {missing_symbols}"
                )

            objs: List[LevelTwo] = []
            now = datetime.now(timezone.utc)
            skipped_count = 0

            for b in batch:
                sec_id = symbol_to_id.get(b.get("symbol"))
                if not sec_id:
                    skipped_count += 1
                    continue

                side_str = b.get("side") or ""
                side_val = (
                    OrderSide(side_str) if side_str in ("BID", "ASK") else OrderSide.BID
                )
                price_level_int = self._to_price_int(b.get("price_level"))
                size_int = self._to_int(b.get("size"))
                order_count_val = int(b.get("order_count") or 0)
                level_index_val = int(b.get("level_index") or 0)

                # Enforce model constraints (>0) to avoid DB errors
                if not price_level_int or price_level_int <= 0:
                    skipped_count += 1
                    continue
                if not size_int or size_int <= 0:
                    skipped_count += 1
                    continue
                if order_count_val <= 0:
                    skipped_count += 1
                    continue

                obj = LevelTwo(
                    security_id=sec_id,
                    timestamp=now,
                    instrument_type=InstrumentType.EQUITY,
                    side=side_val,
                    price_level=price_level_int,
                    size=size_int,
                    order_count=order_count_val,
                    level_index=level_index_val,
                    market_maker_id=(b.get("market_maker_id") or None),
                    mic_id=(b.get("mic_id") or None),
                    quote_time=self._to_int(b.get("quote_time")),
                )
                objs.append(obj)

            if objs:
                self.logger.info(
                    f"Saving {len(objs)} L2 records to database (skipped {skipped_count} invalid)"
                )
                db.add_all(objs)
                await db.commit()
                self.logger.debug("L2 batch commit successful")
            else:
                self.logger.warning(
                    f"No valid L2 objects created from batch of {len(batch)} items (skipped {skipped_count})"
                )

    async def _flush_charts(self, batch: List[Dict[str, Any]]) -> None:
        if not batch:
            return

        self.logger.info(f"Flushing chart batch with {len(batch)} items")

        symbols = sorted({b["symbol"] for b in batch if b.get("symbol")})
        async with AsyncSessionLocal() as db:
            symbol_to_id = await self._resolve_security_ids(db, symbols)
            missing_symbols = [s for s in symbols if not symbol_to_id.get(s)]
            if missing_symbols:
                self.logger.warning(
                    f"Missing security IDs for chart symbols: {missing_symbols}"
                )

            # Prepare normalized rows keyed by (security_id, timestamp, timeframe)
            from sqlalchemy import select, tuple_, update

            def parse_chart_timestamp(raw_ts: Any) -> datetime:
                if raw_ts is None:
                    return datetime.now(timezone.utc)
                try:
                    if isinstance(raw_ts, (int, float)):
                        # Heuristic: milliseconds vs seconds
                        ts_sec = float(raw_ts) / (
                            1000.0 if float(raw_ts) > 1e11 else 1.0
                        )
                        return datetime.fromtimestamp(ts_sec, tz=timezone.utc)
                    if isinstance(raw_ts, str):
                        try:
                            dt = datetime.fromisoformat(raw_ts)
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=timezone.utc)
                            return dt
                        except Exception:
                            # Fallback: try numeric string
                            num = float(raw_ts)
                            ts_sec = num / (1000.0 if num > 1e11 else 1.0)
                            return datetime.fromtimestamp(ts_sec, tz=timezone.utc)
                except Exception:
                    pass
                return datetime.now(timezone.utc)

            normalized: Dict[tuple, Dict[str, Any]] = {}
            skipped_count = 0

            for b in batch:
                sec_id = symbol_to_id.get(b.get("symbol"))
                if not sec_id:
                    skipped_count += 1
                    continue

                open_price_int = self._to_price_int(b.get("open_price"))
                high_price_int = self._to_price_int(b.get("high_price"))
                low_price_int = self._to_price_int(b.get("low_price"))
                close_price_int = self._to_price_int(b.get("close_price"))
                volume_int = self._to_int(b.get("volume"))

                # Skip if missing critical OHLC data or invalid values
                if not all(
                    [open_price_int, high_price_int, low_price_int, close_price_int]
                ):
                    skipped_count += 1
                    continue
                if any(
                    p <= 0
                    for p in [
                        open_price_int,
                        high_price_int,
                        low_price_int,
                        close_price_int,
                    ]
                ):
                    skipped_count += 1
                    continue

                if volume_int is None or volume_int < 0:
                    volume_int = 0

                timeframe_raw = b.get("timeframe", "1m")
                try:
                    timeframe_enum = Timeframe(timeframe_raw)
                except ValueError:
                    timeframe_enum = Timeframe.ONE_MINUTE
                timeframe_val = timeframe_enum.value

                ts = parse_chart_timestamp(b.get("timestamp"))

                key = (sec_id, ts, timeframe_val)
                normalized[key] = {
                    "security_id": sec_id,
                    "timestamp": ts,
                    "timeframe": timeframe_val,
                    "instrument_type": InstrumentType.EQUITY,
                    "open_price": open_price_int,
                    "high_price": high_price_int,
                    "low_price": low_price_int,
                    "close_price": close_price_int,
                    "volume": volume_int,
                    "trade_count": self._to_int(b.get("trade_count")),
                    "vwap": self._to_price_int(b.get("vwap")),
                    "is_regular_hours": True,
                }

            if not normalized:
                self.logger.warning(
                    f"No valid chart objects created from batch of {len(batch)} items (skipped {skipped_count})"
                )
                return

            keys = list(normalized.keys())
            # Find which keys already exist
            existing_keys: set[tuple] = set()
            if keys:
                result = await db.execute(
                    select(Chart.security_id, Chart.timestamp, Chart.timeframe).where(
                        tuple_(Chart.security_id, Chart.timestamp, Chart.timeframe).in_(
                            keys
                        )
                    )
                )
                existing_keys = set(result.fetchall())

            # Split into inserts and updates
            inserts: List[Chart] = []
            updates: List[Dict[str, Any]] = []

            for key, row in normalized.items():
                if key in existing_keys:
                    updates.append(row)
                else:
                    inserts.append(
                        Chart(
                            security_id=row["security_id"],
                            timestamp=row["timestamp"],
                            timeframe=row["timeframe"],
                            instrument_type=row["instrument_type"],
                            open_price=row["open_price"],
                            high_price=row["high_price"],
                            low_price=row["low_price"],
                            close_price=row["close_price"],
                            volume=row["volume"],
                            trade_count=row["trade_count"],
                            vwap=row["vwap"],
                            is_regular_hours=row["is_regular_hours"],
                        )
                    )

            # Perform updates
            updated_count = 0
            for row in updates:
                await db.execute(
                    update(Chart)
                    .where(
                        (Chart.security_id == row["security_id"])
                        & (Chart.timestamp == row["timestamp"])
                        & (Chart.timeframe == row["timeframe"])
                    )
                    .values(
                        open_price=row["open_price"],
                        high_price=row["high_price"],
                        low_price=row["low_price"],
                        close_price=row["close_price"],
                        volume=row["volume"],
                        trade_count=row["trade_count"],
                        vwap=row["vwap"],
                        is_regular_hours=row["is_regular_hours"],
                    )
                )
                updated_count += 1

            # Perform inserts (triggers partition ensure via ORM event)
            if inserts:
                db.add_all(inserts)

            await db.commit()

            self.logger.info(
                f"Charts upserted: {len(inserts)} inserted, {updated_count} updated (skipped {skipped_count})"
            )

    async def _resolve_security_ids(
        self, db: AsyncSession, symbols: List[str]
    ) -> Dict[str, Optional[Any]]:
        # Use cache when available
        missing = [s for s in symbols if s not in self._security_cache]
        if missing:
            from sqlalchemy import select

            result = await db.execute(
                select(Security.symbol, Security.id).where(Security.symbol.in_(missing))
            )
            found: Dict[str, Any] = {row[0]: row[1] for row in result.fetchall()}
            for s in missing:
                self._security_cache[s] = found.get(s)
        return {s: self._security_cache.get(s) for s in symbols}

    def _to_price_int(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        try:
            # Store prices with 1e4 precision to preserve sub-cent decimals
            return int(round(float(value) * 10_000))
        except Exception:
            return None

    def _to_int(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        try:
            return int(float(value))
        except Exception:
            return None

    # ---------- Error-handling enqueue methods ----------
    async def _enqueue_l1_batch(self, entities: List[Dict[str, Any]]) -> None:
        """Safely enqueue L1 entities with error handling."""
        if not self._l1_batcher:
            self.logger.error("L1 batcher is None, cannot enqueue entities")
            return
        try:
            for ent in entities:
                await self._l1_batcher.add(ent)
        except Exception as e:
            self.logger.error(f"Failed to enqueue L1 entities: {type(e).__name__}: {e}")
            # Don't re-raise to avoid breaking the message handler

    async def _enqueue_l2_batch(self, entities: List[Dict[str, Any]]) -> None:
        """Safely enqueue L2 entities with error handling."""
        if not self._l2_batcher:
            self.logger.error("L2 batcher is None, cannot enqueue entities")
            return
        try:
            for ent in entities:
                await self._l2_batcher.add(ent)
        except Exception as e:
            self.logger.error(f"Failed to enqueue L2 entities: {type(e).__name__}: {e}")
            # Don't re-raise to avoid breaking the message handler

    async def _enqueue_chart_batch(self, entities: List[Dict[str, Any]]) -> None:
        """Safely enqueue chart entities with error handling."""
        if not self._chart_batcher:
            self.logger.error("Chart batcher is None, cannot enqueue entities")
            return
        try:
            for ent in entities:
                await self._chart_batcher.add(ent)
        except Exception as e:
            self.logger.error(
                f"Failed to enqueue chart entities: {type(e).__name__}: {e}"
            )
            # Don't re-raise to avoid breaking the message handler
