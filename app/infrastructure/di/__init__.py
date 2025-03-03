from typing import List

from dishka import Provider

from .bot import BotProvder, DispatcherProvider
from .config import ConfigProvider
from .db import DatabaseProvider
from .repository import RepositoryProvider
from .interactors import InteractorsProvider
from .utils import UtilsProvider
from .fast_stream import FastStreamProvider


def get_bot_providers() -> List[Provider]:
    return [
        BotProvder(),
        DispatcherProvider(),
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        InteractorsProvider(),
        UtilsProvider(),
        FastStreamProvider()
    ]

def get_stream_providers() -> List[Provider]:
    return [
        BotProvder(),
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        InteractorsProvider(),
        UtilsProvider(),
        FastStreamProvider()
    ]


__all__ = [
    "get_stream_providers",
    "get_bot_providers"
]