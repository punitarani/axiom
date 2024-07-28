"""axiom/ws/equity_level_one.py"""

import asyncio
import ssl
from pathlib import Path

from httpx import Response
from schwab.client import AsyncClient
from schwab.streaming import StreamClient

from axiom.schwab_client import (
    SCHWAB_APP_KEY,
    SCHWAB_REDIRECT_URI,
    SCHWAB_SECRET,
    SCHWAB_TOKEN_FP,
    get_schwab_client,
    sch_limiter,
)
from axiom.schwab_models import LevelOneEquity
from axiom.store.cache import level_one_cache


class EquityLevelOneStream:

    def __init__(self, queue_size: int = 100, symbols=None):
        self.api_key: str = SCHWAB_APP_KEY
        self.client_secret: str = SCHWAB_SECRET
        self.callback_url: str = SCHWAB_REDIRECT_URI
        self.token_path: Path = SCHWAB_TOKEN_FP

        self.account_id = None
        self.account_hash = None

        self.schwab_client = None
        self.stream_client = None

        self.symbols: list[str] = symbols or ["SPY", "QQQ"]

        # Create a queue so we can queue up work gathered from the client
        self.queue: asyncio.Queue[LevelOneEquity] = asyncio.Queue(queue_size)

    async def initialize(self):
        """Create the streaming client"""
        sch = get_schwab_client()

        self.schwab_client: AsyncClient = sch

        async with sch_limiter:
            account_info_data: Response = await self.schwab_client.get_account_numbers()
            account_info = account_info_data.json()

        self.account_id = int(account_info[0]["accountNumber"])
        self.account_hash = account_info[0]["hashValue"]

        # Disable SSL verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        self.stream_client = StreamClient(
            client=self.schwab_client, account_id=self.account_id, ssl_context=ssl_context
        )

        # Add the handlers for each service type
        self.stream_client.add_level_one_equity_handler(self.handle_level_one_equity)

    async def stream(self):
        await self.stream_client.login()

        # TODO: QOS is currently not working as the command formatting has changed.
        #  Update & re-enable after docs are released
        # await self.stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)

        # Subscribe to the symbols for each service type
        await self.stream_client.level_one_equity_subs(self.symbols)

        # Kick off our handle_queue function as an independent coroutine
        asyncio.ensure_future(self.handle_queue())

        # Continuously handle inbound messages
        while True:
            await self.stream_client.handle_message()

    async def handle_level_one_equity(self, msg):
        """
        This is where we take msgs from the streaming client and put them on a
        queue for later consumption. We use a queue to prevent us from wasting
        resources processing old data, and falling behind.
        """

        data = LevelOneEquity.model_validate(msg)

        # if the queue is full, make room
        if self.queue.full():  # This won't happen if the queue doesn't have a max size
            print("Handler queue is full. Awaiting to make room... Some messages might be dropped")
            await self.queue.get()
        await self.queue.put(data)

    async def handle_queue(self):
        """
        Here we pull messages off the queue and process them.
        """
        while True:
            msg = await self.queue.get()

            match msg.service:
                case "LEVELONE_EQUITIES":
                    # Store the data in the cache
                    for i, symbol in enumerate(msg.content):
                        level_one_cache[symbol.key] = msg.content[i].model_dump_json()
                case _:
                    print(f"Unhandled message: {msg}")


async def run_equity_level_one_stream():
    """
    Create and instantiate the consumer, and start the stream
    """
    consumer = EquityLevelOneStream()

    await consumer.initialize()
    await consumer.stream()


if __name__ == "__main__":
    asyncio.run(run_equity_level_one_stream())
