from pydantic import (
    BaseModel, 
    SecretStr, 
    model_validator
)


class BotConfig(BaseModel):
    token: SecretStr

    @model_validator(mode="before")
    def check_token(cls, data: dict) -> dict:
        if data.get("token") == "":
            raise AssertionError("Token is not set")
        return data

class DatabaseConfig(BaseModel):
    user: str
    password: SecretStr
    host: str = "db"
    port: int = 5432
    path: str
    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def make_connection_url(self) -> str:
        return (
            f"{self.database_system}+{self.driver}://"
            f"{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.path}"
        )
    
class NatsConfig(BaseModel):
    host: str = "nats"
    port: int = 4222
    user: str | None = None
    password: SecretStr | None = None

    def build_connection_url(self) -> str:
        return (
            f"nats://{self.user}:{self.password.get_secret_value() if self.password else ''}"
            f"@{self.host}:{self.port}"
        )
    
class DebugConfig(BaseModel):
    log_level: int = 10
    json_logs: bool = False
    
class Config(BaseModel):
    bot: BotConfig
    db: DatabaseConfig
    nats: NatsConfig
    debug: DebugConfig
