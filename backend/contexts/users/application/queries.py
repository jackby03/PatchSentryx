import uuid

from pydantic import BaseModel, EmailStr, Field


# --- Query DTOs ---
class UserDTO(BaseModel):
    """Data Transfer Object for User information."""

    id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# --- Query Models (Optional, if you need specific query parameters) ---


class GetUserByIdQuery(BaseModel):
    """Represents the parameters needed for the GetUserById query."""

    user_id: uuid.UUID


class ListUsersQuery(BaseModel):
    """Represents parameters for listing users (e.g., pagination, filtering)."""

    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    is_active: bool | None = None  # Example filter
