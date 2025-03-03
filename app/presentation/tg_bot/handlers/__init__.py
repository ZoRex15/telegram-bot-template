from aiogram import Router

from .commands import router as start_router


handler_router = Router()
handler_router.include_router(start_router)

__all__ = [
    "handler_router"
]