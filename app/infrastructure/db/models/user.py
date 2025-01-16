from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, VARCHAR, TIMESTAMP, func

from app.infrastructure.db.models.base import Base
from app.core.dtos import UserDTO


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    username: Mapped[str] = mapped_column(VARCHAR(128), nullable=True, index=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)

    def __str__(self) -> str:
        return (
            "UserModel("
            f"id={self.id}, "
            f"tg_id={self.tg_id}, "
            f"username={self.username}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"created_at={self.created_at})"
        )
    
    def to_dto(self) -> UserDTO:
        return UserDTO(
            id=self.id,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            created_at=self.created_at
        )
    
    @classmethod
    def from_dto(cls, dto: UserDTO):
        return User(
            id=dto.id,
            tg_id=dto.tg_id,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            created_at=dto.created_at
        )


    