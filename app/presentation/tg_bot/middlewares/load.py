from typing import Any, Awaitable, Callable, Dict
from datetime import datetime

from dishka import AsyncContainer

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as AiogramUser

from app.application.users.create_user import CreateUser, CreateUserDTO
from app.application.users.get_user_by_tg_id import GetUserByTgId
from app.core.exceptions.users import UserNotFound


class LoadMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        aiogram_user: AiogramUser = data.get("event_from_user")
        if aiogram_user:
            try:
                dishka: AsyncContainer = data.get("dishka_container")
                get_user_by_tg_id: GetUserByTgId = await dishka.get(GetUserByTgId)
                db_user = await get_user_by_tg_id(aiogram_user.id)
            except UserNotFound:
                create_user: CreateUser = await dishka.get(CreateUser)
                db_user = await create_user(
                    CreateUserDTO(
                        tg_id=aiogram_user.id,
                        first_name=aiogram_user.first_name,
                        last_name=aiogram_user.last_name,
                        username=aiogram_user.username,
                        created_at=datetime.now()
                    )
                )
            data["user"] = db_user
        return await handler(event, data)
        