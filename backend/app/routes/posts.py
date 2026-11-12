from pathlib import Path
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

from app.database import get_session
from app.models import Post
from app.schemas.post import PostRead
from app.core.dependencies import get_current_user
from app.models import User


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