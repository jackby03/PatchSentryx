import json
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.responses import JSONResponse

from contexts.users.application.commands import CreateUserCommand
from contexts.users.application.queries import (GetUserByIdQuery,
                                                ListUsersQuery, UserDTO)
from contexts.users.infrastructure.messaging import UserCommandPublisher
from contexts.users.interfaces.dependencies import (CreateUserHandler,
                                                    GetUserByIdHandler,
                                                    ListUsersHandler)
from core.dependencies import MqChannel
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()


@router.post(
    "/",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user (via async command handler)",
    description="Accepts user registration details and publish a command to create the user.",
)
async def register_user_command(
    channel: MqChannel,
    command_data: CreateUserCommand = Body(...),
):
    publisher = UserCommandPublisher(channel)

    try:
        command = CreateUserCommand(**command_data.model_dump())
        await publisher.publish_create_user_command(command)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": "User creation request accepted.",
                "email": command.email,
            },
        )
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error publishing create user command: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user create command.",
        )


@router.get(
    "/{user_id}",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
async def get_user(
    user_id: uuid.UUID,
    handler: GetUserByIdHandler,
):
    query = GetUserByIdQuery(user_id=user_id)
    try:
        user_dto = await handler.handle(query)
        if user_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_dto
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error getting user by ID {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user.",
        )


@router.get(
    "/",
    response_model=List[UserDTO],
    status_code=status.HTTP_200_OK,
    summary="List users",
)
async def list_users(
    handler: ListUsersHandler,
    query_params: ListUsersQuery = Depends(),
):
    try:
        user_dtos = await handler.handle(query_params)
        return user_dtos
    except Exception as e:
        print(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing users.",
        )
