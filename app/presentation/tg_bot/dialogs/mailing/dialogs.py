from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Jinja
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.input import MessageInput

from app.presentation.tg_bot import states

from .handlers import message_handler, delete_image, start_mailing
from .gatters import create_mailing_getter


mailing_dialog = Dialog(
    Window(
        Const("Выберете действие"),
        SwitchTo(
            Const("Создать рассылку"),
            id="create_mailing",
            state=states.Mailing.CREATE_MAILING
        ),
        Cancel(text=Const("Назад")),
        state=states.Mailing.MAILING_MENU
    ),
    Window(
        Const("Создание рассылки"),
        Const("Отправте текст или фото чтобы задать его для рассылки"),
        Jinja("Текст рассылки: <blockquote>{{ text }}</blockquote>"),
        DynamicMedia(
            selector="image",
            when="image"
        ),
        MessageInput(
            func=message_handler
        ),
        Button(
            id="delete_image",
            text=Const("🗑️ Удалить изображение"),
            when="image",
            on_click=delete_image,
        ),
        Button(
            id="start_mailing",
            text=Const("Начать рассылку"),
            on_click=start_mailing,
            when="sending_allowed"
        ),
        SwitchTo(
            text=Const("Назад"),
            id="back",
            state=states.Mailing.MAILING_MENU
        ),
        getter=create_mailing_getter,
        state=states.Mailing.CREATE_MAILING
    )
)