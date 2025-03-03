from typing import Sequence

from app.infrastructure.db.repository import UsersRepository
from app.core.dtos import UserDTO


class GetAllUsers:
    def __init__(self, repository: UsersRepository) -> None:
        self.repository = repository

    async def __call__(self) -> Sequence[UserDTO]:
        return await self.repository.get_all()
