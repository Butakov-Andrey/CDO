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
    # gpt
    VSEGPT_API_KEY: str
    VSEGPT_BASE_URL: str = "https://api.vsegpt.ru/v1"
    # timezone
    moscow_timezone: tzinfo = pytz.timezone("Europe/Moscow")
    # logging
    LOGURU_FORMAT: str = (
        "<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
    )
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE"))


class GptSettings:
    MODEL = "mistralai/mixtral-8x7b-instruct"
    TEMPERATURE: float = 0.7
    N: int = 1
    MAX_TOKENS: int = 3000


class Prompts:
    SYSTEM_PROMPT = """
You're a helpfull assistant.
Determine the mood of the feedback, depending on the hints:
Hints:
"positive" - the feedback is positive.
"negative" - the feedback is negative.
"neutral" - the feedback is neutral.
and the next feedback text from the user:
FEEDBACK TEXT FROM THE USER:
"""
    ANSWER_PROMPT = """
Provide your response as a JSON:
{
    "sentiment": <mood_of_the_feedback>
}
"""


settings = Settings()
gpt_settings = GptSettings()
prompts = Prompts()
