from dishka import Provider, provide, Scope

from app.infrastructure.utils.broker import BrokerAdapter


class UtilsProvider(Provider):
    scope = Scope.APP

    broker_adapter = provide(BrokerAdapter)