from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import MailingStatus
from app.core.types import MailingId


class MailingDTO(BaseModel):
    text: str

    id: Optional[MailingId] = None
    status: MailingStatus = MailingStatus.CREATED
    created_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    tg_image_id: Optional[str] = None 


class MailingMetadataDTO(BaseModel):
    pending_notifications_count: int
    text: str
    tg_image_id: Optional[str] = None 
    status: MailingStatus = MailingStatus.CREATED

