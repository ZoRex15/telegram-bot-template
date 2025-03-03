import asyncio
import logging
import os
import sys

from datetime import timedelta

import nats
import nats.js
from nats.js.api import StreamConfig, RetentionPolicy, StorageType, DiscardPolicy, KeyValueConfig
import nats.js.kv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.infrastructure.config import get_config

logger = logging.getLogger(__name__)


async def main():
    logger.info('start nats migrations')
    config = get_config()
    nc = await nats.connect(servers=config.nats.build_connection_url())
    js = nc.jetstream()
    await js.add_stream(
        config=StreamConfig(
            name='mailing',
            subjects=[
                "mailing.*.start",
                "mailing.*.send.message.*"
            ],
            retention=RetentionPolicy.LIMITS,  
            storage=StorageType.FILE,
            max_msgs=10_000,
            max_age=13_200,
            discard=DiscardPolicy.NEW,
            num_replicas=1,
            max_bytes=10_485_760,
            max_msgs_per_subject=1
        )
    )
    await js.create_key_value(
        KeyValueConfig(
            bucket="mailing_storage",
            ttl=timedelta(hours=48).seconds
        )
    )
    await nc.close()
    logger.info('end nats migrations')


asyncio.run(main())