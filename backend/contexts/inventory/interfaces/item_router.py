import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body
from starlette.responses import JSONResponse

from contexts.inventory.application.commands import CreateItemCommand
from contexts.inventory.application.queries import (
    ItemDTO,
)
from contexts.inventory.infrastructure.messaging import InventoryCommandPublisher
from core.dependencies import MqChannel
from core.errors import DomainError

router = APIRouter()

# --- Command Endpoints ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new item (via async command)",
    description="Accepts item creation details and publishes a command to create the item asynchronously."
)
async def create_item(
        channel: MqChannel,
        command_data: CreateItemCommand = Body(...),
):
    publisher = InventoryCommandPublisher(channel)
    try:
        command = CreateItemCommand(**command_data.model_dump())
        await publisher.publish_create_item(command)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": "Item creation request accepted.",
                "item_id": command.item_id,
            },
        )
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error publishing create user command: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


@router.put("/{item_id}", response_model=ItemDTO)
async def update_item():
    raise


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item():
    raise

# --- Query Endpoints ---
@router.get("", response_model=List[ItemDTO])
async def list_items():
    raise


@router.get("/{item_id}", response_model=ItemDTO)
async def get_item():
    raise

