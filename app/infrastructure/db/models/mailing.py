from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Enum, TIMESTAMP, TEXT, VARCHAR, func

from app.infrastructure.db.models.base import Base
from app.core.dtos import MailingDTO
from app.core.enums import MailingStatus


class Mailing(Base):
    __tablename__ = "Mailings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    tg_image_id: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)
    text: Mapped[str] = mapped_column(TEXT, nullable=False)

    status: Mapped[MailingStatus] = mapped_column(Enum(MailingStatus), nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    ended_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    def __str__(self) -> str:
        return (
            "MailingModel("
            f"id={self.id}, "
            f"tg_image_id={self.tg_image_id}, "
            f"text={self.text}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"ended_at={self.ended_at})"
        )
    
    def to_dto(self) -> MailingDTO:
        return MailingDTO(
            id=self.id,
            tg_image_id=self.tg_image_id,
            text=self.text,
            status=self.status,
            created_at=self.created_at,
            ended_at=self.ended_at
        )
       
    @classmethod
    def from_dto(cls, dto: MailingDTO):
        return Mailing(
            id=dto.id,
            tg_image_id=dto.tg_image_id,
            text=dto.text,
            status=dto.status,
            created_at=dto.created_at,
            ended_at=dto.ended_at
        )