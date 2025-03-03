from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from dishka.integrations.aiogram_dialog import inject
from dishka import FromDishka

from app.application.mailing.create import CreateMailing, CreateMailingDTO


async def message_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    if message.text or message.caption:
        dialog_manager.dialog_data["data_text"] = message.text or message.caption
    if message.photo:
        dialog_manager.dialog_data["data_image_id"] = message.photo[-1].file_id

async def delete_image(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    dialog_manager.dialog_data["data_image_id"] = None


@inject
async def start_mailing(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    create_mailing: FromDishka[CreateMailing]
):
    mailing = await create_mailing(
        CreateMailingDTO(
            text=dialog_manager.dialog_data.get("data_text"),
            tg_image_id=dialog_manager.dialog_data["data_image_id"]
        )
    )
    await callback.message.answer(
        text=(
            "✅ Рассылка запущена!\n"
            f"Уникальный ID рассылки: <code>{mailing.id}</code>"
        )
    )
    await dialog_manager.back()