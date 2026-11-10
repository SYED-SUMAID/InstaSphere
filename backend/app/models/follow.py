from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint


class Follow(SQLModel, table=True):

    __tablename__ = "userfollow"

    __table_args__ = (
        CheckConstraint(
            "follower_id != followed_id",
            name="prevent_self_follow"
        ),
    )

    follower_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        primary_key=True
    )

    followed_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        primary_key=True
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    follower: "User" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "Follow.follower_id"}
    )

    followed: "User" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "Follow.followed_id"}
    )