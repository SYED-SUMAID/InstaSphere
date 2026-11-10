from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship



class Comment(SQLModel, table=True):

    __tablename__ = "comment"

    id: int | None = Field(default=None, primary_key=True)

    text: str

    commenter_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        index=True
    )

    post_id: int = Field(
        foreign_key="post.id",
        ondelete="CASCADE",
        index=True
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    commenter: "User" = Relationship(back_populates="comments")

    post: "Post" = Relationship(back_populates="comments")