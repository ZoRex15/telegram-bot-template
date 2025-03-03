import logging

from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from app.infrastructure.db.repository import MailingsRepository
from app.infrastructure.db.uow import UnitOfWork
from app.core.enums import MailingStatus
from app.core.dtos import MailingDTO
from app.application.base import Interactor

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class UpdateMailingDTO:
    id: int
    status: MailingStatus
    ended_at: Optional[datetime] = None

class UpdateMailing(Interactor[UpdateMailingDTO, MailingDTO]):
    def __init__(self, repository: MailingsRepository, uow: UnitOfWork) -> None:
        self.repository = repository
        self.uow = uow

    async def __call__(self, data: UpdateMailingDTO) -> MailingDTO:
        mailing = await self.repository.get_mailing_by_id(data.id)
        if mailing is None:
            raise
        async with self.uow:
            mailing = await self.repository.update_mailing(
                MailingDTO(
                    id=data.id,
                    text=mailing.text,
                    tg_image_id=mailing.tg_image_id,
                    status=data.status,
                    created_at=mailing.created_at,
                    ended_at=data.ended_at
                )
            )
            await self.uow.commit()
            logger.info("Mailing was updated", extra={"mailing": mailing})
            return mailing