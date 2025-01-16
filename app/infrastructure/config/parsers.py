from environs import Env

from app.infrastructure.config.models import (
    NatsConfig,
    DatabaseConfig,
    DebugConfig,
    BotConfig,
    Config
)


def get_nats_config(env: Env) -> NatsConfig:
    return NatsConfig(
        host=env.str("NATS_HOST", "nats"),
        port=env.int("NATS_PORT", 4222),
        user=env.str("NATS_USER", None),
        password=env.str("NATS_PASSWORD", None)
    )

def get_database_config(env: Env) -> DatabaseConfig:
    return DatabaseConfig(
        user=env.str("DB_USER"),
        password=env.str("DB_PASSWORD"),
        host=env.str("DB_HOST", "db"),
        port=env.int("DB_PORT", 5432),
        path=env.str("DB_PATH"),
        driver=env.str("DB_DRIVER", "asyncpg"),
        database_system=env.str("DB_SYSTEM", "postgresql")
    )

def get_debug_config(env: Env) -> DebugConfig:
    return DebugConfig(
        log_level=env.int("DEBUG_LOG_LEVEL", 10),
        json_logs=env.bool("DEBUG_JSON_LOGS", False)
    )

def get_bot_config(env: Env) -> BotConfig:
    return BotConfig(
        token=env.str("BOT_TOKEN"),
    )

def get_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        nats=get_nats_config(env),
        debug=get_debug_config(env),
        db=get_database_config(env),
        bot=get_bot_config(env)
    )


