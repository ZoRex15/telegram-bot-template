import logging

from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from app.infrastructure.db.repository import MailingsRepository
from app.infrastructure.db.uow import UnitOfWork
from app.infrastructure.utils.broker import BrokerAdapter
from app.core.enums import MailingStatus
from app.core.dtos import MailingDTO
from app.application.base import Interactor
from app.presentation.stream.consumers.mailing.create import MailingStartDTO

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CreateMailingDTO:
    text: str
    tg_image_id: Optional[str] = None 

class CreateMailing(Interactor[CreateMailingDTO, MailingDTO]):
    def __init__(
        self, 
        repository: MailingsRepository, 
        uow: UnitOfWork,
        broker: BrokerAdapter,
    ) -> None:
        self.repository = repository
        self.uow = uow
        self.broker = broker

    async def __call__(self, data: CreateMailingDTO) -> MailingDTO:
        async with self.uow:
            mailing = await self.repository.create_mailing(
                MailingDTO(
                    id=None,
                    text=data.text,
                    tg_image_id=data.tg_image_id,
                    status=MailingStatus.CREATED,
                    created_at=datetime.now(),
                    ended_at=None
                )
            )
            await self.broker.mailing_start(MailingStartDTO(mailing_id=mailing.id))
            await self.uow.commit()
            logger.info("New mailing created", extra={"mailing": mailing})
            return mailing