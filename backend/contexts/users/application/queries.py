import uuid
from typing import List

from pydantic import BaseModel, EmailStr, Field

# --- Query DTOs ---
# These represent the data structure returned by queries.
# They might differ from domain entities (e.g., omitting sensitive fields like password).


class UserDTO(BaseModel):
    """Data Transfer Object for User information."""

    id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True  # Enable creating DTO from ORM/domain objects


# --- Query Models (Optional, if you need specific query parameters) ---


class GetUserByIdQuery(BaseModel):
    """Represents the parameters needed for the GetUserById query."""

    user_id: uuid.UUID


class ListUsersQuery(BaseModel):
    """Represents parameters for listing users (e.g., pagination, filtering)."""

    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    is_active: bool | None = None  # Example filter
