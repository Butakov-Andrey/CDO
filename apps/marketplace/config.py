import os
from datetime import tzinfo

import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # timezone
    moscow_timezone: tzinfo = pytz.timezone("Europe/Moscow")
    # logging
    LOGURU_FORMAT: str = (
        "<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
    )
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE"))


settings = Settings()
