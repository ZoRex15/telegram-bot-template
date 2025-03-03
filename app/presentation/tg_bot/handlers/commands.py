from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from aiogram_dialog import DialogManager, StartMode

from app.presentation.tg_bot import states


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hi!")

@router.message(Command("mailing_menu"))
async def send_mailing_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.Mailing.MAILING_MENU, mode=StartMode.RESET_STACK)