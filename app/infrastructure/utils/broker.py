from __future__ import annotations

from typing import TYPE_CHECKING

from faststream.nats import NatsBroker
from tenacity import retry, stop_after_attempt, wait_exponential

if TYPE_CHECKING:
    from app.presentation.stream.consumers.mailing.create import MailingStartDTO
    from app.presentation.stream.consumers.mailing.send_notification import MailingSendMessageDTO
        



class BrokerAdapter:
    def __init__(self, broker: NatsBroker) -> None:
        self.broker = broker

    async def mailing_start(self, data: MailingStartDTO) -> None:
        await self.broker.publish(data, subject=f"mailing.{data.mailing_id}.start")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def mailing_send_message(self, data: MailingSendMessageDTO) -> None:
        await self.broker.publish(data, subject=f"mailing.{data.mailing_id}.send.message.{data.user.id}")