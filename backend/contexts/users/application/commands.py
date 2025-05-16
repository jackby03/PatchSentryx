import uuid

from pydantic import BaseModel, EmailStr, Field


class CreateUserCommand(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, description="User password (plain text)")


class UpdateUserCommand(BaseModel):
    user_id: uuid.UUID
    name: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None


class DeleteUserCommand(BaseModel):
    user_id: uuid.UUID
