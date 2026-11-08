from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.database import get_session
from app.models import User
from app.core.security import decode_access_token


# ==========================================
# OAUTH2 CONFIGURATION
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================
# GET CURRENT AUTHENTICATED USER
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Decode and validate JWT
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    # Extract user ID from JWT subject
    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise credentials_exception

    # Find user in PostgreSQL
    user = session.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user