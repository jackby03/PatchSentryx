import uuid

from pydantic import BaseModel, EmailStr, Field

# --- Command DTOs ---
# These are simple data structures representing the intent to change the system state.


class CreateUserCommand(BaseModel):
    """Command to create a new user."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, description="User password (plain text)")
    # Optionally add a command ID for tracking/idempotency
    # command_id: uuid.UUID = Field(default_factory=uuid.uuid4)


class UpdateUserCommand(BaseModel):
    """Command to update an existing user (example)."""

    user_id: uuid.UUID
    name: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None


class DeleteUserCommand(BaseModel):
    """Command to delete a user (example)."""

    user_id: uuid.UUID


# Other commands can be defined here, e.g., ChangeUserPasswordCommand
