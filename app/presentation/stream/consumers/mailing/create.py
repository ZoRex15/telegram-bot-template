import asyncio

from pydantic import BaseModel

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.nats import NatsRouter, JStream
from faststream.nats.annotations import NatsMessage

from app.application.users.get_all_users import GetAllUsers
from app.application.mailing.get_by_id import GetMailingById
from app.application.mailing.save_metadata import SaveMailingMetadata, SaveMailingMetadataDTO
from app.core.enums import MailingStatus
from app.core.types import MailingId
from app.infrastructure.utils.broker import BrokerAdapter
from app.presentation.stream.consumers.mailing.send_notification import MailingSendMessageDTO

router = NatsRouter()


class MailingStartDTO(BaseModel):
    mailing_id: MailingId

@router.subscriber(
    "mailing.*.start",
    durable="mailing_load_users",
    stream=JStream("mailing", declare=False),
    no_ack=True
)
@inject
async def mailing_load_users(
    msg: MailingStartDTO,
    nats_msg: NatsMessage,
    get_all_users: FromDishka[GetAllUsers],
    save_mailing_metadata: FromDishka[SaveMailingMetadata],
    get_mailing_by_id: FromDishka[GetMailingById],
    broker: FromDishka[BrokerAdapter],
):
    mailing = await get_mailing_by_id(msg.mailing_id)
    if mailing != MailingStatus.STOPPED:
        users = await get_all_users()
        tasks = [
            broker.mailing_send_message(
                MailingSendMessageDTO(
                    mailing_id=msg.mailing_id,
                    user=user
                )
            )
            for user in users
        ]
        await asyncio.gather(*tasks)
        await save_mailing_metadata(
            SaveMailingMetadataDTO(
                mailing_id=msg.mailing_id,
                text=mailing.text,
                tg_image_id=mailing.tg_image_id,
                pending_notifications_count=len(users)
            )
        )
    await nats_msg.ack()
