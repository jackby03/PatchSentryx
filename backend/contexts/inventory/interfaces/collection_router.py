import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from contexts.inventory.application.commands import (
    CreateCollectionCommand,
    DeleteCollectionCommand,
    UpdateCollectionCommand,
)
from contexts.inventory.application.queries import (
    CollectionDTO,
    GetItemsByCollectionQuery,
    ItemDTO,
    ListActiveCollectionsQuery,
    ListCollectionsQuery,
)
from contexts.inventory.interfaces.dependencies import (
    CreateCollectionHandler,
    DeleteCollectionHandler,
    GetItemsByCollectionHandler,
    ListActiveCollectionsHandler,
    ListCollectionsHandler,
    UpdateCollectionHandler,
)

router = APIRouter(prefix="/collections", tags=["collections"])

# --- Query Endpoints ---


@router.get("", response_model=List[CollectionDTO])
async def list_collections(
    handler: ListCollectionsHandler,
):
    # List all collections
    return await handler.handle(ListCollectionsQuery())


@router.get("/active", response_model=List[CollectionDTO])
async def list_active_collections(
    handler: ListActiveCollectionsHandler,
):
    # List only active collections
    return await handler.handle(ListActiveCollectionsQuery())


@router.post("", response_model=CollectionDTO, status_code=status.HTTP_201_CREATED)
async def create_collection(
    cmd: CreateCollectionCommand,
    create_handler: CreateCollectionHandler,
    list_handler: ListCollectionsHandler,
):
    # Create new collection
    try:
        await create_handler.handle(cmd)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
        ) from ve

    # Return the newly created collection by matching name
    cols = await list_handler.handle(ListCollectionsQuery())
    for c in cols:
        if c.name == cmd.name:
            return c
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Created collection not found.",
    )


@router.put("/{collection_id}", response_model=CollectionDTO)
async def update_collection(
    collection_id: uuid.UUID,
    cmd: UpdateCollectionCommand,
    update_handler: UpdateCollectionHandler,
    list_handler: ListCollectionsHandler,
):
    # Ensure path and body IDs match
    if cmd.id != collection_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID mismatch."
        )
    try:
        await update_handler.handle(cmd)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ve)
        ) from ve
    # Return updated collection
    cols = await list_handler.handle(ListCollectionsQuery())
    for c in cols:
        if c.id == collection_id:
            return c
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Updated collection not found.",
    )


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: uuid.UUID,
    delete_handler: DeleteCollectionHandler,
    cmd: DeleteCollectionCommand,
):
    # Validate ID
    if cmd.id != collection_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID mismatch."
        )
    try:
        await delete_handler.handle(cmd)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ve)
        ) from ve


@router.get("/{collection_id}/items", response_model=List[ItemDTO])
async def list_items_in_collection(
    collection_id: uuid.UUID,
    query_handler: GetItemsByCollectionHandler,
):
    # Retrieve items for a collection
    items = await query_handler.handle(
        GetItemsByCollectionQuery(collection_id=collection_id)
    )
    return items
