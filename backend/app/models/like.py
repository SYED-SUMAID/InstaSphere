from datetime import datetime

from sqlmodel import SQLModel, Field


class Like(SQLModel, table=True):

    __tablename__ = "liketracker"

    liker_id: int = Field(
        foreign_key="user.id",
        primary_key=True
    )

    post_id: int = Field(
        foreign_key="post.id",
        primary_key=True
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )