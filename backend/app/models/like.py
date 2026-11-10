from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Like(SQLModel, table=True):

    __tablename__ = "liketracker"

    liker_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        primary_key=True
    )

    post_id: int = Field(
        foreign_key="post.id",
        ondelete="CASCADE",
        primary_key=True
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    liker: "User" = Relationship(back_populates="likes")

    post: "Post" = Relationship(back_populates="likes")