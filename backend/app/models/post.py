from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship



class Post(SQLModel, table=True):

    __tablename__ = "post"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        index=True
    )

    caption: str | None = Field(default=None)

    image_path: str = Field(max_length=500)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="posts")

    comments: list["Comment"] = Relationship(back_populates="post")

    likes: list["Like"] = Relationship(back_populates="post")