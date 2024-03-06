from datetime import datetime

from config import settings
from feedback.schema import FeedbackSchema
from pydantic import BaseModel, validator


class ProductSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    feedbacks: list[FeedbackSchema]

    @validator("created_at", pre=True)
    def created_at_validate(cls, created_at):
        if created_at:
            return created_at.astimezone(settings.moscow_timezone)
        return created_at


class CreateProductSchema(BaseModel):
    name: str


class UpdateProductSchema(BaseModel):
    name: str | None = None
    created_at: datetime | None = None
