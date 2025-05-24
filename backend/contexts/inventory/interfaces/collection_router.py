import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status, Body, Depends

from contexts.inventory.application.commands import CreateCollectionCommand
from contexts.inventory.application.queries import (
    CollectionDTO,
    GetCollectionByIdQuery,
    ListCollectionsQuery,
)
from contexts.users.infrastructure.messaging import UserCommandPublisher
from core.dependencies import MqChannel
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()


# --- Command Endpoints ---
@router.post(
    "/",
    response_model=CollectionDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new collection",
    description="Accepts collection creation details and creates a new collection in the database.",
)
async def create_collection(
    channel: MqChannel,
    command_data: CreateCollectionCommand = Body(...),
):
    publisher = UserCommandPublisher(channel)
    try:
        command = CreateCollectionCommand(**command_data.model_dump())
        raise Exception("Not yet implemented")
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


@router.put(
    "/{collection_id}",
    response_model=CollectionDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Update a collection",
    description="Accepts collection update details and updates an existing collection in the database.",
)
async def update_collection(
    channel: MqChannel,
    command_data: CreateCollectionCommand = Body(...),
):
    publisher = UserCommandPublisher(channel)
    try:
        command = CreateCollectionCommand(**command_data.model_dump())
        raise Exception("Not yet implemented")
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


@router.delete(
    "/{collection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a collection",
    description="Accepts collection ID and deletes the corresponding collection from the database.",
)
async def delete_collection(
    channel: MqChannel,
    collection_id: uuid.UUID,
):
    publisher = UserCommandPublisher(channel)
    try:
        raise Exception("Not yet implemented")
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


# --- Query Endpoints ---
@router.get(
    "/{collection_id}",
    response_model=CollectionDTO,
    status_code=status.HTTP_200_OK,
    summary="List collections",
    description="Retrieves a list of collections from the database.",
)
async def get_collection(collection_id: uuid.UUID, handler: GetCollectionByIdQuery):
    query = GetCollectionByIdQuery(collection_id=collection_id)
    try:
        collection_dto = await handler.handle(query)
        if collection_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
            )
        return collection_dto
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error getting collection by ID {collection_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the collection.",
        )


@router.get(
    "/",
    response_model=List[CollectionDTO],
    status_code=status.HTTP_200_OK,
    summary="List collections",
    description="Retrieves a list of collections from the database.",
)
async def list_collections(
    handler: ListCollectionsQuery,
    query_params: ListCollectionsQuery = Depends(),
):
    try:
        collection_dtos = await handler.handle(query_params)
        return collection_dtos
    except Exception as e:
        print(f"Error listing collections: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing collections.",
        )
