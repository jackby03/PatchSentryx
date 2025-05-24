import uuid
from typing import List

from pydantic import BaseModel, Field

# --- Command DTOs ---
# These are simple data structures representing the intent to change the system state.


class CreateItemCommand(BaseModel):
    """Command to create a new item."""

    name: str = Field(..., min_length=1, max_length=100)
    hostname: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., min_length=1, max_length=100)
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)


class UpdateItemCommand(BaseModel):
    """Command to update an existing item (example)."""

    id: uuid.UUID
    name: str | None = Field(None, min_length=1, max_length=100)
    hostname: str | None = Field(None, min_length=1, max_length=100)
    version: str | None = Field(None, min_length=1, max_length=100)
    brand: str | None = Field(None, min_length=1, max_length=100)
    model: str | None = Field(None, min_length=1, max_length=100)
    serial_number: str | None = Field(None, min_length=1, max_length=100)
    location: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None


class DeleteItemCommand(BaseModel):
    """Command to delete an item (example)."""

    id: uuid.UUID
