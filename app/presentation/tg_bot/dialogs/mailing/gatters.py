from aiogram.enums import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId


async def create_mailing_getter(dialog_manager: DialogManager, **kwargs):
    text = dialog_manager.dialog_data.get("data_text")
    image = None
    if file_id := dialog_manager.dialog_data.get("data_image_id"):
        image = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(file_id)
        )
    return {
        "text": text,
        "image": image,
        "sending_allowed": True if text else False
    }