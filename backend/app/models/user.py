from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(max_length=255)
    username: str = Field(max_length=100, unique=True, index=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)

    bio: str | None = Field(default=None)
    profile_picture: str | None = Field(default=None, max_length=255)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    posts: list["Post"] = Relationship(back_populates="user")

    comments: list["Comment"] = Relationship(back_populates="commenter")