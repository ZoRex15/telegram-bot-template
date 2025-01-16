from dishka import Provider, provide, Scope

from environs import Env

from app.infrastructure.config import (
    NatsConfig,
    DatabaseConfig,
    DebugConfig,
    BotConfig,
    get_database_config,
    get_nats_config,
    get_debug_config,
    get_bot_config
)


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, env: Env) -> DatabaseConfig:
        return get_database_config(env)
    
    @provide
    def get_nats_config(self, env: Env) -> NatsConfig:
        return get_nats_config(env)

    @provide
    def get_debug_config(self, env: Env) -> DebugConfig:
        return get_debug_config(env)
    
    @provide
    def get_bot_config(self, env: Env) -> BotConfig:
        return get_bot_config(env)
    
    @provide
    def get_env(self) -> Env:
        env = Env()
        env.read_env()
        return env