from pydantic import BaseModel

from dishka import FromDishka
from dishka.integrations.faststream import inject

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
)

from faststream import Logger
from faststream.nats import NatsRouter, JStream, PullSub
from faststream.nats.annotations import NatsMessage

from app.application.mailing.get_metadata_by_id import GetMailingMetadataById
from app.core.dtos.user import UserDTO
from app.core.types import MailingId

router = NatsRouter()


class MailingSendMessageDTO(BaseModel):
    mailing_id: MailingId
    user: UserDTO

@router.subscriber(
    "mailing.*.send.message.*",
    durable="mailing_send_message",
    pull_sub=PullSub(batch_size=30),
    stream=JStream("mailing", declare=False),
    no_ack=True
)
@inject
async def mailing_send_message(
    msg: MailingSendMessageDTO,
    nats_msg: NatsMessage,
    logger: Logger,
    bot: FromDishka[Bot],
    get_mailing_metadata_by_id: FromDishka[GetMailingMetadataById]
):
    try:
        mailing = await get_mailing_metadata_by_id(msg.mailing_id)
        if mailing.tg_image_id:
            await bot.send_photo(
                chat_id=msg.user.tg_id,
                photo=mailing.tg_image_id,
                caption=mailing.text
            )
        else:
            await bot.send_message(
                chat_id=msg.user.tg_id,
                caption=mailing.text
            )
    except TelegramRetryAfter as error:
        await nats_msg.nack(delay=error.retry_after)
        logger.warning(
            "Retrying sending a message to %s in %s", msg.user.id, error.retry_after
        )
        return
    except (TelegramBadRequest, TelegramForbiddenError) as error:
        await nats_msg.reject()
        logger.info("Skipping sending message to %s", msg.user.id, exc_info=error)
        return
    else:
        await nats_msg.ack()
    return