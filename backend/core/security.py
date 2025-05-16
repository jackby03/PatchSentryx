from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Password Hashing Context
# Use bcrypt as the default hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


# JWT Token Handling
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    # Add 'iat' (issued at) claim
    to_encode.update({"iat": datetime.now(timezone.utc)})
    # Add 'sub' (subject) claim if not present (conventionally user identifier)
    # Ensure 'sub' is always present and is a string
    if "sub" not in to_encode or not isinstance(to_encode["sub"], str):
        # Fallback or raise error if subject logic is missing
        # For example, use email if available, otherwise raise
        if "email" in to_encode and isinstance(to_encode["email"], str):
            to_encode["sub"] = to_encode["email"]
        else:
            # Or simply use a default placeholder if appropriate, but usually identifier is key
            # to_encode['sub'] = 'default_subject' # Or raise error
            raise ValueError(
                "Subject ('sub') claim missing or not a string in token data"
            )

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optionally add more validation here (e.g., check 'aud' claim)
        return payload
    except JWTError:
        # Handles various errors like expired signature, invalid signature, etc.
        return None
