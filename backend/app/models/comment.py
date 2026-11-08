from datetime import datetime

from sqlmodel import SQLModel, Field


class Comment(SQLModel, table=True):

    __tablename__ = "comment"

    id: int | None = Field(default=None, primary_key=True)

    text: str

    commenter_id: int = Field(
        foreign_key="user.id"
    )

    post_id: int = Field(
        foreign_key="post.id"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )