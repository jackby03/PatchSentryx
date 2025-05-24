import uuid

from pydantic import BaseModel


class ItemDTO(BaseModel):
    """DTO for returning item information to the client."""

    id: uuid.UUID
    name: str
    hostname: str
    version: str
    brand: str
    model: str
    serial_number: str
    location: str
    user_id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True


# --- Query Models (Optional, if you need specific query parameters) ---


class GetItemByIdQuery(BaseModel):
    """Represents the parameters needed for the GetItemById query."""

    item_id: uuid.UUID


class ListItemsQuery(BaseModel):
    """Represents parameters for listing items (e.g., pagination, filtering)."""

    limit: int = 100
    offset: int = 0
    is_active: bool | None = None
