from datetime import datetime

from config import settings
from pydantic import BaseModel, validator


class FeedbackSchema(BaseModel):
    id: int
    text: str
    created_at: datetime
    sentiment: str
    product_id: int

    @validator("created_at", pre=True)
    def created_at_validate(cls, created_at):
        if created_at:
            return created_at.astimezone(settings.moscow_timezone)
        return created_at


class CreateFeedbackSchema(BaseModel):
    text: str
