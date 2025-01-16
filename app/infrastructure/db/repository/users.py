from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.db.models import User
from app.core.dtos import UserDTO


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, dto: UserDTO) -> UserDTO:
        user = User.from_dto(dto)
        self.session.add(user)
        await self.session.flush([user])
        return user.to_dto()
    
    async def update_user(self, dto: UserDTO) -> UserDTO:
        user = await self.session.merge(User.from_dto(dto))
        await self.session.flush([user])
        return user.to_dto()
    
    async def get_user_by_id(self, id: int) -> UserDTO | None:
        user = (
            await self.session.execute(
                select(User)
                .where(User.id == id)
            )
        ).scalar()
        return user.to_dto() if user else None
    
    async def get_user_by_tg_id(self, tg_id: int) -> UserDTO | None:
        user = (
            await self.session.execute(
                select(User)
                .where(User.tg_id == tg_id)
            )
        ).scalar()
        return user.to_dto() if user else None
    
    

        