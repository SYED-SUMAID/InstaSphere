from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import settings


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """

    password_bytes = password.encode("utf-8")

    # Bcrypt supports a maximum of 72 password bytes.
    if len(password_bytes) > 72:
        raise ValueError("Password cannot exceed 72 bytes")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


# ==========================================
# PASSWORD VERIFICATION
# ==========================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against its bcrypt hash.
    """

    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except (ValueError, TypeError):
        return False


# ==========================================
# JWT TOKEN GENERATION
# ==========================================

def create_access_token(data: dict) -> str:
    """
    Generate a JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    access_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return access_token


# ==========================================
# JWT TOKEN VERIFICATION
# ==========================================

def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate a JWT access token.

    Returns the token payload if valid.
    Returns None if invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None