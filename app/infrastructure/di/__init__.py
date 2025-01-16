from typing import List

from dishka import Provider

from .bot import BotProvder, DispatcherProvider
from .config import ConfigProvider
from .db import DatabaseProvider
from .repository import RepositoryProvider
from .interactors import InteractorsProvider


def get_bot_providers() -> List[Provider]:
    return [
        BotProvder(),
        DispatcherProvider(),
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        InteractorsProvider()
    ]

def get_stream_providers() -> List[Provider]:
    return [
        BotProvder(),
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        InteractorsProvider()
    ]


__all__ = [
    "get_stream_providers",
    "get_bot_providers"
]