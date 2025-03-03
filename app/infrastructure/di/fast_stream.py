from typing import AsyncIterable

from dishka import Provider, Scope, provide

from faststream.nats import NatsBroker

from app.infrastructure.config import NatsConfig
from app.core.types import MailingKeyValueStorage
from app.presentation.stream.consumers.mailing import mailing_router


class FastStreamProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_broker(self, config: NatsConfig) -> AsyncIterable[NatsBroker]:
        broker = NatsBroker(
            servers=config.build_connection_url()
        )
        broker.include_router(mailing_router)
        await broker.connect()
        yield broker
        await broker.close()

    @provide
    async def get_mailing_key_value_storage(self, broker: NatsBroker) -> MailingKeyValueStorage: 
        return await broker.key_value("mailing_storage", declare=False)
