from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    caption: str | None = None


class PostRead(BaseModel):
    id: int
    user_id: int
    caption: str | None
    image_path: str
    created_at: datetime
    updated_at: datetime