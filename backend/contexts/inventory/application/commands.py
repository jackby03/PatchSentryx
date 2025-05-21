import uuid
from typing import List

from pydantic import BaseModel, Field


# --- Create / Update Item ---
class CreateItemCommand(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    hostname: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., min_length=1, max_length=100)
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    collection_id: uuid.UUID


class UpdateItemCommand(CreateItemCommand):
    id: uuid.UUID


# --- Delete Item ---
class DeleteItemCommand(BaseModel):
    id: uuid.UUID


# --- Item Status ---
class UpdateItemStatusCommand(BaseModel):
    id: uuid.UUID
    is_active: bool


# --- Move Items between Collections ---
class MoveItemsCommand(BaseModel):
    item_ids: List[uuid.UUID]
    target_collection_id: uuid.UUID


# --- Create / Update Collection ---
class CreateCollectionCommand(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)


class UpdateCollectionCommand(CreateCollectionCommand):
    id: uuid.UUID


# --- Delete Collection ---
class DeleteCollectionCommand(BaseModel):
    id: uuid.UUID
    delete_items: bool = True
