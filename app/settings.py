from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    AAPI_HOST: str
    AAPI_TOKEN: SecretStr

    WEBHOOK_HOST: str
    WEBHOOK_PATH: str = "/webhook"
    TELEGRAM_SECRET: SecretStr = "mysecretpassword"

    POSTGRES_HOST: str
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: SecretStr
    REDIS_DB: int

    CHECK_EDBO: bool = False
    KM_RADIUS: int = 2
    LAT: float = 50.447322
    LON: float = 30.459321

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"

    model_config = SettingsConfigDict(
        env_file=('stack.env', '.env'),
        extra="ignore"
    )


settings = Settings()
