from dishka import Provider, Scope, provide, AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from app.presentation.tg_bot.handlers import handler_router
from app.presentation.tg_bot.middlewares import LoadMiddleware
from app.infrastructure.config import BotConfig


class BotProvder(Provider):
    scope = Scope.APP

    @provide
    def get_bot(self, config: BotConfig) -> Bot:
        return Bot(
            token=config.token.get_secret_value(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )
    
class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    def get_dispatcher(self, dishka: AsyncContainer) -> Dispatcher:
        dp = Dispatcher()
        dp.include_router(handler_router)
        dp.update.middleware(LoadMiddleware())
        setup_dishka(dishka, dp, auto_inject=True)
        return dp

    @provide
    def get_storage(self) -> BaseStorage:
        return MemoryStorage()