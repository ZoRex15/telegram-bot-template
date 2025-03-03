import logging

from typing import Optional
from dataclasses import dataclass

from app.core.dtos import MailingMetadataDTO
from app.core.types import MailingKeyValueStorage, MailingId
from app.core.enums import MailingStatus
from app.application.base import Interactor

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SaveMailingMetadataDTO:
    mailing_id: MailingId
    text: str
    pending_notifications_count: int
    
    tg_image_id: Optional[str] = None 

class SaveMailingMetadata(Interactor[SaveMailingMetadataDTO, None]):
    def __init__(self, storage: MailingKeyValueStorage) -> None:
        self.storage = storage

    async def __call__(self, data: SaveMailingMetadataDTO) -> None:
        await self.storage.put(
            key=str(data.mailing_id),
            value=MailingMetadataDTO(
                pending_notifications_count=data.pending_notifications_count,
                tg_image_id=data.tg_image_id,
                text=data.text,
            ).model_dump_json().encode()
        )
        logger.info("Mailing %s metadata created", data.mailing_id)