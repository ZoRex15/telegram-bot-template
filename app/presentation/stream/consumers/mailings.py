# import asyncio

# from pydantic import BaseModel

# from dishka import FromDishka

# from aiogram import Bot
# from aiogram.exceptions import (
#     TelegramBadRequest,
#     TelegramForbiddenError,
#     TelegramRetryAfter,
# )

# from faststream import Logger
# from faststream.nats import NatsRouter, JStream, PullSub, ConsumerConfig
# from faststream.nats.annotations import NatsBroker, NatsMessage

# from app.application.users.get_all_users import GetAllUsers
# from app.application.users.get_user_by_id import GetUserById
# from app.application.mailing.get_by_id import GetMailingById
# from app.application.mailing.save_metadata import SaveMailingMetadata, SaveMailingMetadataDTO
# from app.application.mailing.get_metadata_by_id import GetMailingMetadataById
# from app.application.mailing.update import UpdateMailing, UpdateMailingDTO
# from app.application.mailing.delete_metadata import MailingDeleteMetadata
# from app.core.enums import MailingStatus
# from app.core.types import MailingId
# from app.infrastructure.utils.broker import BrokerAdapter


# router = NatsRouter()

# class MailingStartDTO(BaseModel):
#     mailing_id: MailingId

# @router.subscriber(
#     "mailing.*.start",
#     durable="mailing_load_users",
#     stream=JStream("mailing", declare=False),
#     no_ack=True
# )
# async def mailing_load_users(
#     msg: MailingStartDTO,
#     nats_msg: NatsMessage,
#     get_all_users: FromDishka[GetAllUsers],
#     save_mailing_metadata: FromDishka[SaveMailingMetadata],
#     get_mailing_by_id: FromDishka[GetMailingById],
#     broker: FromDishka[BrokerAdapter],
# ):
#     mailing = await get_mailing_by_id(msg.mailing_id)
#     if mailing != MailingStatus.STOPPED:
#         users = await get_all_users()
#         tasks = [
#             broker.mailing_send_message(
#                 MailingSendMessageDTO(
#                     mailing_id=msg.mailing_id,
#                     user_id=user.id
#                 )
#             )
#             for user in users
#         ]
#         await asyncio.gather(*tasks)
#         await save_mailing_metadata(
#             SaveMailingMetadataDTO(
#                 mailing_id=msg.mailing_id,
#                 from_chat_id=mailing.from_chat_id,
#                 message_id=mailing.message_id,
#                 pending_notifications_count=len(users),
#                 status=mailing.status
#             )
#         )
#     await nats_msg.ack()


# class MailingSendMessageDTO(BaseModel):
#     mailing_id: MailingId
#     user_id: int

# @router.subscriber(
#     "mailing.*.send.message.*",
#     durable="mailing_send_message",
#     pull_sub=PullSub(batch_size=30),
#     stream=JStream("mailing", declare=False),
#     no_ack=True,
#     config=ConsumerConfig(
        
#     )
# )
# async def mailing_send_message(
#     msg: MailingSendMessageDTO,
#     nats_msg: NatsMessage,
#     logger: Logger,
#     bot: FromDishka[Bot],
#     get_user_by_id: FromDishka[GetUserById],
#     get_mailing_metadata_by_id: FromDishka[GetMailingMetadataById],
#     save_mailing_metadata: FromDishka[SaveMailingMetadata]
# ):
#     try:
#         mailing = await get_mailing_metadata_by_id(msg.mailing_id)
#         if mailing.status == MailingStatus.STOPPED:
#             await nats_msg.reject()
#         user = await get_user_by_id(msg.user_id)
#         await bot.copy_message(
#             chat_id=user.tg_id,
#             from_chat_id=mailing.from_chat_id,
#             message_id=mailing.message_id
#         )
#         mailing.pending_notifications_count -= 1
#         await save_mailing_metadata(SaveMailingMetadataDTO(**mailing.model_dump()))
#         if mailing.pending_notifications_count == 0:
#             pass
#     except TelegramRetryAfter as error:
#         await nats_msg.nack(delay=error.retry_after)
#         logger.warning(
#             "Retrying sending a message to %s in %s", msg.user_id, error.retry_after
#         )
#         return
#     except (TelegramBadRequest, TelegramForbiddenError) as error:
#         await nats_msg.reject()
#         logger.info("Skipping sending message to %s", msg.user_id, exc_info=error)
#         return
#     else:
#         await nats_msg.ack()
#     return


# class MailingIsOverDTO(BaseModel):
#     mailing_id: MailingId

# @router.subscriber(
#     "mailing.*.over",
#     durable="mailing_is_over",
#     pull_sub=PullSub(batch_size=30),
#     stream=JStream("mailing", declare=False),
#     no_ack=True
# )
# async def mailing_is_over(
#     msg: MailingIsOverDTO,
#     nats_msg: NatsMessage,
#     logger: Logger,
#     bot: FromDishka[Bot],
#     get_mailing_by_id: FromDishka[GetMailingById],
#     update_mailing: FromDishka[UpdateMailing],
#     delete_mailing_metadata: FromDishka[MailingDeleteMetadata],
# ):
#     mailing = await get_mailing_by_id(msg.mailing_id)
#     await update_mailing(
        
#     )