from faststream.nats import NatsRouter

from .create import router as create_router
from .send_notification import router as send_notification_router


mailing_router = NatsRouter()
mailing_router.include_routers(
    create_router,
    send_notification_router
)


__all__ = [
    "mailing_router"
]