from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import select
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status
)
from sqlmodel import Session
from app.schemas.post import PostRead, PostUpdate
from app.database import get_session
from app.models import Post
from app.schemas.post import PostRead
from app.core.dependencies import get_current_user
from app.models import User
from fastapi import Body
from app.models import Post, Like
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

# Backend upload directory
BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads" / "posts"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    caption: str | None = Form(default=None),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG and WEBP images are allowed"
        )

    extension = ALLOWED_TYPES[image.content_type]
    filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / filename

    image_data = await image.read()

    if not image_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty"
        )

    file_path.write_bytes(image_data)

    new_post = Post(
        user_id=current_user.id,
        caption=caption,
        image_path=f"uploads/posts/{filename}"
    )

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post

@router.get("/", response_model=list[PostRead])
def get_all_posts(
    session: Session = Depends(get_session)
):
    posts = session.exec(
        select(Post).order_by(Post.created_at.desc())
    ).all()

    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this post"
        )

    image_file = (BASE_DIR / post.image_path).resolve()

    if UPLOAD_DIR.resolve() in image_file.parents and image_file.is_file():
        image_file.unlink()

    session.delete(post)
    session.commit()

    return {"message": "Post deleted successfully"}


@router.patch("/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this post"
        )

    if "caption" in post_data.model_fields_set:
        post.caption = post_data.caption

    post.updated_at = datetime.now(timezone.utc)

    session.add(post)
    session.commit()
    session.refresh(post)

    return post

@router.post("/{post_id}/like", status_code=201)
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    existing_like = session.get(
        Like,
        (current_user.id, post_id)
    )

    if existing_like:
        raise HTTPException(
            status_code=409,
            detail="You have already liked this post"
        )

    new_like = Like(
        liker_id=current_user.id,
        post_id=post_id
    )

    session.add(new_like)
    session.commit()

    return {"message": "Post liked successfully"}

@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    existing_like = session.get(
        Like,
        (current_user.id, post_id)
    )

    if not existing_like:
        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )

    session.delete(existing_like)
    session.commit()

    return {"message": "Post unliked successfully"}

@router.get("/{post_id}/likes")
def get_post_likes(
    post_id: int,
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    likes_count = session.exec(
        select(func.count())
        .select_from(Like)
        .where(Like.post_id == post_id)
    ).one()

    return {
        "post_id": post_id,
        "likes_count": likes_count
    }