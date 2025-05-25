import uuid
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from contexts.inventory.application.commands import (
    CreateItemCommand,
)
from contexts.inventory.application.queries import ItemDTO, ListItemsQuery
from contexts.inventory.application.query_handlers import (
    CreateItemHandler,
    GetItemByIdHandler,
)
from contexts.inventory.interfaces.dependencies import ListItemsHandler
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()


# --- Direct Command Handling Endpoint
@router.post("/", response_model=ItemDTO)
async def create_item_sync(
    handler: CreateItemHandler,
    command: CreateItemCommand = Body(...),  # noqa: B008
):
    try:
        created_item = await handler.handle(command)
        return ItemDTO.model_validate(created_item)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error creating item synchronously: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item creation.",
        )


@router.put(
    "/{item_id}",
    response_model=ItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Update an existing item",
    description="Updates the details of an existing item by its ID.",
)
async def update_item(
    item_id: uuid.UUID,
    handler: GetItemByIdHandler,
    command: CreateItemCommand = Body(...),  # noqa: B008
):
    try:
        command.id = item_id  # Set the ID for the update
        updated_item = await handler.handle(command)
        return ItemDTO.model_validate(updated_item)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error updating item {item_id}: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item update.",
        )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Deletes an item by its ID.",
)
async def delete_item(
    item_id: uuid.UUID,
    handler: GetItemByIdHandler,
):
    try:
        command = CreateItemCommand(item_id=item_id)  # Create a command with the ID
        await handler.handle(command)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error deleting item {item_id}: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during item deletion.",
        )


# --- Query Endpoints ---
@router.get(
    "/{item_id}",
    response_model=ItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Get item by ID",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Item not found"}},
)
async def get_item(
    item_id: uuid.UUID,
    handler: GetItemByIdHandler,
):
    """
    Retrieves item details by their unique ID.
    """
    try:
        item_dto = await handler.handle(item_id)
        if item_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return ItemDTO.model_validate(item_dto)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error getting item by ID {item_id}: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the item.",
        )


@router.get(
    "/",
    response_model=List[ItemDTO],
    status_code=status.HTTP_200_OK,
    summary="List items",
)
async def list_items(
    handler: ListItemsHandler,
    query_params: ListItemsQuery = Depends(),  # noqa: B008
):
    """
    Lists all items.
    """
    try:
        item_dtos = await handler.handle(query_params)
        return item_dtos
    except Exception as e:
        print(f"Error listing items: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing items.",
        )
