import uuid

from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    """
    Domain Entity representing an Inventory Item.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    hostname: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., min_length=1, max_length=100)
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    user_id: uuid.UUID = Field(...)
    is_active: bool = True

    class Config:
        from_attributes = True
        orm_mode = True

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty.")
        return v
