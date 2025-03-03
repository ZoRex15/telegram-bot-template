import logging

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from app.application.base import Interactor
from app.infrastructure.db.repository import UsersRepository
from app.infrastructure.db.uow import UnitOfWork
from app.core.dtos import UserDTO

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    tg_id: int
    created_at: datetime = datetime.now()

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class CreateUser(Interactor):
    def __init__(self, repository: UsersRepository, uow: UnitOfWork) -> None:
        self.repository = repository
        self.uow = uow

    async def __call__(self, data: CreateUserDTO) -> UserDTO:
        async with self.uow:
            user = await self.repository.create_user(
                UserDTO(
                    tg_id=data.tg_id,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    username=data.username,
                    created_at=data.created_at,
                    id=None
                )
            )
            await self.uow.commit()
            logger.info("New user created", extra={"user": user})
            return user
