from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.schemas.token import Token
from app.core.security import hash_password, verify_password, create_access_token


# ==========================================
# AUTHENTICATION ROUTER
# ==========================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# USER REGISTRATION
# ==========================================

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):

    # Check whether username or email already exists
    existing_user = session.exec(
        select(User).where(
            (User.username == user_data.username) |
            (User.email == user_data.email)
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered"
        )

    # Hash the user's password
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    # Save user to PostgreSQL
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


# ==========================================
# USER LOGIN
# ==========================================

@router.post("/login", response_model=Token)
def login_user(
    user_data: UserLogin,
    session: Session = Depends(get_session)
):

    # Find user using email
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    # Check whether user exists and password matches
    if not user or not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generate JWT access token
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }