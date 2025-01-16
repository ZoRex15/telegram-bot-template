from app.application.base import Interactor
from app.infrastructure.db.repository import UsersRepository
from app.core.dtos import UserDTO
from app.core.exceptions.users import UserNotFound


class GetUserByTgId(Interactor[int, UserDTO]):
    def __init__(self, repository: UsersRepository) -> None:
        self.repository = repository

    async def __call__(self, data: int) -> UserDTO:
        if user := await self.repository.get_user_by_tg_id(data):
            return user
        raise UserNotFound
        