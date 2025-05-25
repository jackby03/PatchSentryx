import json  # noqa: F401
import uuid
from typing import Annotated, List  # noqa: F401

from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.responses import JSONResponse  # noqa: F401

from contexts.users.application.commands import CreateUserCommand
from contexts.users.application.queries import GetUserByIdQuery, ListUsersQuery, UserDTO
from contexts.users.infrastructure.messaging import (
    UserCommandPublisher,  # noqa: F401
)  # Import publisher logic
from contexts.users.interfaces.dependencies import (  # Use handler dependencies directly now; UserCmdPublisher, # Dependency for direct publishing if needed
    CreateUserHandler,
    GetUserByIdHandler,
    ListUsersHandler,
)
from core.dependencies import (
    MqChannel,  # noqa: F401
)  # Import channel dependency for direct publishing
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()


# --- Direct Command Handling Endpoint ---
@router.post(
    "/",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user (synchronously)",
    description="Handles user registration directly without message queue.",
)
async def create_user_sync(
    handler: CreateUserHandler,  # Inject the command handler
    command: CreateUserCommand = Body(...),  # noqa: B008
):
    try:
        created_user = await handler.handle(command)
        return UserDTO.model_validate(created_user)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))  # noqa: B904
    except Exception as e:
        # Log the exception e
        print(f"Error creating user synchronously: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user creation.",
        )


# --- Command Endpoints Asynchronous ---
@router.post(
    "/async/",
    response_model=UserDTO,  # Return DTO of the created user
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user (via async command)",
    description="Accepts user registration details and publishes a command to create the user asynchronously.",
)
async def register_user_command(
    # Option 1: Get channel and publisher manually
    # channel: MqChannel,
    # command_data: CreateUserCommand = Body(...),  # noqa: B008
    # Option 2: Inject publisher directly (if publisher dependency is set up)
    publisher: UserCommandPublisher,
    command_data: CreateUserCommand = Body(...),  # noqa: B008
):
    """
    Handles the request to create a new user by publishing a command to RabbitMQ.
    """
    # publisher = UserCommandPublisher(channel)  # Manual instantiation with channel
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error publishing create user command: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


# --- Query Endpoints ---


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
    """
    Retrieves user details by their unique ID.
    """
    query = GetUserByIdQuery(user_id=user_id)
    try:
        user_dto = await handler.handle(query)
        if user_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_dto
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  # noqa: B904
    except Exception as e:
        print(f"Error getting user by ID {user_id}: {e}")
        # Log the exception
        raise HTTPException(  # noqa: B904
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
    query_params: ListUsersQuery = Depends(),  # noqa: B008
):
    """
    Retrieves a list of users, potentially with filtering and pagination.
    """
    try:
        user_dtos = await handler.handle(query_params)
        return user_dtos
    except Exception as e:
        print(f"Error listing users: {e}")
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing users.",
        )
