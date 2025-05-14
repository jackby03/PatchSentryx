import uuid

from pydantic import BaseModel, EmailStr, Field

class UserDTO(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class GetUserByIdQuery(BaseModel):
    user_id: uuid.UUID

class ListUsersQuery(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    is_active: bool | None = None