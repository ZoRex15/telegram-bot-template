import logging

from app.core.types import MailingKeyValueStorage, MailingId
from app.core.dtos import MailingMetadataDTO
from app.application.base import Interactor

logger = logging.getLogger(__name__)


class MailingDeleteMetadata(Interactor[MailingId, MailingMetadataDTO]):
    def __init__(self, kv_storage: MailingKeyValueStorage) -> None:
        self.kv_storage = kv_storage

    async def __call__(self, data: MailingId) -> MailingMetadataDTO:
        await self.kv_storage.delete(str(data))
        logger.info("Mailing %s metadata deleted", data)
