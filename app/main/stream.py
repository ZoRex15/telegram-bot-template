import asyncio

from faststream import FastStream
from faststream.nats import NatsBroker

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka

from app.infrastructure.config.models import DebugConfig
from app.infrastructure.di import get_stream_providers
from app.common.logging import setup_logging


async def main():
    dishka = make_async_container(*get_stream_providers())
    debug_config = await dishka.get(DebugConfig)
    setup_logging(debug_config.log_level, debug_config.json_logs)
    broker: NatsBroker = await dishka.get(NatsBroker)
    app = FastStream(broker=broker)
    setup_dishka(dishka, app, auto_inject=True)
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())

