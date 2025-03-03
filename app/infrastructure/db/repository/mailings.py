from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.db.models import Mailing
from app.core.dtos import MailingDTO


class MailingsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_mailing(self, dto: MailingDTO) -> MailingDTO:
        user = Mailing.from_dto(dto)
        self.session.add(user)
        await self.session.flush([user])
        return user.to_dto()
    
    async def get_mailing_by_id(self, id: int) -> MailingDTO | None:
        mailing = (
            await self.session.execute(
                select(Mailing)
                .where(Mailing.id == id)
            )
        ).scalar()
        return mailing
    
    async def update_mailing(self, dto: MailingDTO) -> MailingDTO:
        mailing = await self.session.merge(Mailing.from_dto(dto))
        await self.session.flush([mailing])
        return mailing.to_dto()
    
    async def get_all_mailings(self) -> Sequence[MailingDTO]:
        mailings = (
            await self.session.execute(
                select(Mailing)
            )
        ).scalars().all()
        return tuple(i.to_dto() for i in mailings)