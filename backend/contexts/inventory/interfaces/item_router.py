import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.inventory.application.commands import (
    CreateItemCommand,
    DeleteItemCommand,
    MoveItemsCommand,
    UpdateItemCommand,
    UpdateItemStatusCommand,
)
from contexts.inventory.application.queries import (
    CountItemsQuery,
    GetItemByIdQuery,
    ItemDTO,
    ListActiveItemsQuery,
    ListItemsQuery,
    SearchItemsQuery,
)
from contexts.inventory.interfaces.dependencies import (
    CountItemsHandler,
    CreateItemHandler,
    DeleteItemHandler,
    GetItemByIdHandler,
    ListActiveItemsHandler,
    ListItemsHandler,
    MoveItemsHandler,
    SearchItemsHandler,
    UpdateItemHandler,
    UpdateItemStatusHandler,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=List[ItemDTO])
async def list_items(
    query: ListItemsQuery = Depends(), handler: ListItemsHandler = Depends()
):
    return await handler.handle(query)


@router.get("/active", response_model=List[ItemDTO])
async def list_active_items(handler: ListActiveItemsHandler = Depends()):
    return await handler.handle(ListActiveItemsQuery(is_active=True))


@router.get("/search", response_model=List[ItemDTO])
async def search_items(
    query: SearchItemsQuery = Depends(), handler: SearchItemsHandler = Depends()
):
    try:
        return await handler.handle(query)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.get("/count", response_model=int)
async def count_items(
    query: CountItemsQuery = Depends(), handler: CountItemsHandler = Depends()
):
    return await handler.handle(query)


@router.get("/{item_id}", response_model=ItemDTO)
async def get_item(item_id: uuid.UUID, handler: GetItemByIdHandler = Depends()):
    try:
        return await handler.handle(GetItemByIdQuery(item_id=item_id))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))


@router.post("", response_model=ItemDTO, status_code=status.HTTP_201_CREATED)
async def create_item(cmd: CreateItemCommand, handler: CreateItemHandler = Depends()):
    try:
        item = await handler.handle(cmd)
        return ItemDTO.model_validate(item)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.put("/{item_id}", response_model=ItemDTO)
async def update_item(
    item_id: uuid.UUID, cmd: UpdateItemCommand, handler: UpdateItemHandler = Depends()
):
    if cmd.id != item_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID mismatch"
        )
    try:
        item = await handler.handle(cmd)
        return ItemDTO.model_validate(item)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: uuid.UUID, handler: DeleteItemHandler = Depends()):
    try:
        await handler.handle(DeleteItemCommand(id=item_id))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))


@router.patch("/{item_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_status(
    item_id: uuid.UUID,
    cmd: UpdateItemStatusCommand,
    handler: UpdateItemStatusHandler = Depends(),
):
    if cmd.id != item_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID mismatch"
        )
    try:
        await handler.handle(cmd)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))


@router.post("/move", response_model=List[uuid.UUID])
async def move_items(cmd: MoveItemsCommand, handler: MoveItemsHandler = Depends()):
    try:
        return await handler.handle(cmd)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
