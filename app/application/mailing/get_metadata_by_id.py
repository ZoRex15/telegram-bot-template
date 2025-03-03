import json

from app.core.types import MailingKeyValueStorage, MailingId
from app.core.dtos import MailingMetadataDTO
from app.application.base import Interactor


class GetMailingMetadataById(Interactor[MailingId, MailingMetadataDTO]):
    def __init__(self, kv_storage: MailingKeyValueStorage) -> None:
        self.kv_storage = kv_storage

    async def __call__(self, data: MailingId) -> MailingMetadataDTO:
        metadata = json.loads((await self.kv_storage.get(str(data))).value.decode())
        return MailingMetadataDTO(**metadata)