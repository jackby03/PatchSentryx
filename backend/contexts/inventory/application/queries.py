import uuid
from typing import Optional

from pydantic import BaseModel, Field


# --- Input Models: parameters for each query ---
class GetItemByIdQuery(BaseModel):
    """Parameters for retrieving a single item by ID."""

    item_id: uuid.UUID


class GetItemsByCollectionQuery(BaseModel):
    """Parameters for retrieving items by collection ID."""

    collection_id: uuid.UUID


class SearchItemsQuery(BaseModel):
    """Parameters for searching items by keyword(s)."""

    query: str = Field(..., min_length=1)


class CountItemsQuery(BaseModel):
    """Parameters for counting items, optionally by active status."""

    is_active: Optional[bool] = None


class ListItemsQuery(BaseModel):
    """Parameters for listing items (pagination, filtering)."""

    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    is_active: Optional[bool] = None


class ListActiveItemsQuery(BaseModel):
    """Parameters for listing items by active status."""

    is_active: bool = Field(True)


class ListCollectionsQuery(BaseModel):
    """Parameters for listing all collections."""

    pass


class ListActiveCollectionsQuery(BaseModel):
    """Parameters for listing collections by active status."""

    is_active: bool = Field(True)


# --- Output DTOs: results returned from queries ---
class ItemDTO(BaseModel):
    """Data Transfer Object for Item information."""

    id: uuid.UUID
    name: str
    hostname: str
    version: str
    brand: str
    model: str
    serial_number: str
    location: str
    collection_id: uuid.UUID

    class Config:
        from_attributes = True


class CollectionDTO(BaseModel):
    """Data Transfer Object for Collection information."""

    id: uuid.UUID
    name: str
    description: str

    class Config:
        from_attributes = True
