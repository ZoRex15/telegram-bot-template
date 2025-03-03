from app.infrastructure.db.repository import MailingsRepository
from app.infrastructure.db.uow import UnitOfWork
from app.core.dtos import MailingDTO
from app.core.types import MailingId
from app.core.exceptions.mailing import MailingNotFound
from app.application.base import Interactor


class GetMailingById(Interactor[MailingId, MailingDTO]):
    def __init__(self, repository: MailingsRepository, uow: UnitOfWork) -> None:
        self.repository = repository
        self.uow = uow

    async def __call__(self, data: MailingId) -> MailingDTO:
        if mailing := await self.repository.get_mailing_by_id(data):
            return mailing
        raise MailingNotFound