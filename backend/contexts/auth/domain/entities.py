from pydantic import BaseModel


class Token(BaseModel):
    """Domain representation of an access token."""

    access_token: str
    token_type: str = "bearer"  # Typically "bearer"


class TokenData(BaseModel):
    """Data extracted from a validated token payload."""

    username: str | None = None  # Usually email or user ID stored in 'sub' claim
    user_id: str | None = None  # Explicit user ID if included in token


# Add other auth-related domain entities if needed, e.g., RefreshToken, Session etc.
