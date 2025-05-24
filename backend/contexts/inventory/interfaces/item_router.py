import uuid
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from contexts.inventory.application.command_handlers import (
    CreateItemCommandHandler,
    DeleteItemCommandHandler,
    UpdateItemCommandHandler,
)
from contexts.inventory.application.commands import (
    CreateItemCommand,
    DeleteItemCommand,
    UpdateItemCommand,
)
from contexts.inventory.application.queries import (
    GetItemByIdQuery,
    ItemDTO,
    ListItemsQuery,
)
from contexts.inventory.applicatoin.query_handlers import (
    GetItemByIdQueryHandler,
    ListItemsQueryHandler,
)
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()


# --- Command Endpoints (direct handling) ---


@router.post(
    "/",
    response_model=ItemDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Accepts item creation details and creates a new item in the database.",
)
async def create_item_sync(
    handler: CreateItemCommandHandler = Depends(),
    command: CreateItemCommand = Body(...),
):
    try:
        created = await handler.handle(command)
        return ItemDTO.model_validate(created)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error creating item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item creation.",
        )


@router.put(
    "/{item_id}",
    response_model=ItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Update an item",
    description="Accepts item update details and updates an existing item in the database.",
)
async def update_item_sync(
    item_id: uuid.UUID,
    handler: UpdateItemCommandHandler = Depends(),
    command: UpdateItemCommand = Body(...),
):
    command.id = item_id
    try:
        updated = await handler.handle(command)
        return ItemDTO.model_validate(updated)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error updating item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item update.",
        )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Deletes the item with the given ID from the database.",
)
async def delete_item_sync(
    item_id: uuid.UUID,
    handler: DeleteItemCommandHandler = Depends(),
):
    command = DeleteItemCommand(id=item_id)
    try:
        await handler.handle(command)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error deleting item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item deletion.",
        )


# --- Query Endpoints ---


@router.get(
    "/{item_id}",
    response_model=ItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Get item by ID",
    description="Retrieves a single item by its unique ID.",
)
async def get_item(
    item_id: uuid.UUID,
    handler: GetItemByIdQueryHandler = Depends(),
):
    query = GetItemByIdQuery(item_id=item_id)
    try:
        dto = await handler.handle(query)
        if dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return dto
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error retrieving item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the item.",
        )


@router.get(
    "/",
    response_model=List[ItemDTO],
    status_code=status.HTTP_200_OK,
    summary="List all items",
    description="Retrieves a list of items, optionally filtered or paginated.",
)
async def list_items(
    handler: ListItemsQueryHandler = Depends(),
    query_params: ListItemsQuery = Depends(),
):
    try:
        return await handler.handle(query_params)
    except Exception as e:
        print(f"Error listing items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing items.",
        )
