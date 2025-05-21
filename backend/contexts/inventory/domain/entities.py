import uuid

from pydantic import BaseModel, Field, field_validator


class InventoryItem(BaseModel):
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
    collection_id: uuid.UUID = Field(...)
    is_active: bool = True

    class Config:
        from_attributes = True

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty.")
        return v
    

class Collection(BaseModel):
    """
    Domain Entity representing a Collection of Inventory Items.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    is_active: bool = True

    class Config:
        from_attributes = True

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty.")
        return v
