import json
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.responses import JSONResponse

from contexts.users.application.commands import CreateUserCommand
from contexts.users.application.queries import (GetUserByIdQuery,
                                                ListUsersQuery, UserDTO)
from contexts.users.infrastructure.messaging import \
    UserCommandPublisher  # Import publisher logic
from contexts.users.interfaces.dependencies import (  # Use handler dependencies directly now; UserCmdPublisher, # Dependency for direct publishing if needed
    CreateUserHandler, GetUserByIdHandler, ListUsersHandler)
from core.dependencies import \
    MqChannel  # Import channel dependency for direct publishing
from core.errors import DomainError, EntityNotFoundError

router = APIRouter()

# --- Command Endpoints ---


@router.post(
    "/",
    response_model=UserDTO,  # Return DTO of the created user
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user (via async command)",
    description="Accepts user registration details and publishes a command to create the user asynchronously.",
)
async def register_user_command(
    # Option 1: Get channel and publisher manually
    channel: MqChannel,
    command_data: CreateUserCommand = Body(...),
    # Option 2: Inject publisher directly (if publisher dependency is set up)
    # publisher: UserCmdPublisher,
    # command_data: CreateUserCommand = Body(...),
):
    """
    Handles the request to create a new user by publishing a command to RabbitMQ.
    """
    publisher = UserCommandPublisher(channel)  # Manual instantiation with channel

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
        # This specific error shouldn't happen here if publishing, but handle just in case
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        # Log the exception
        print(f"Error publishing create user command: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish user creation command.",
        )


# --- Direct Command Handling Endpoint (Alternative/Example) ---
# Use this if you want synchronous user creation via the API for some reason
# @router.post(
#     "/sync",
#     response_model=UserDTO,
#     status_code=status.HTTP_201_CREATED,
#     summary="Register a new user (synchronously)",
#     description="Handles user registration directly without message queue.",
# )
# async def create_user_sync(
#     handler: CreateUserHandler, # Inject the command handler
#     command: CreateUserCommand = Body(...)
# ):
#     try:
#         created_user = await handler.handle(command)
#         return UserDTO.model_validate(created_user)
#     except DomainError as e: # Catch specific domain errors like duplicate email
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
#     except Exception as e:
#         # Log the exception e
#         print(f"Error creating user synchronously: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during user creation.")


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
    handler: GetUserByIdHandler,  # Inject the query handler
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
    except EntityNotFoundError as e:  # Catch specific errors if handler raises them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error getting user by ID {user_id}: {e}")
        # Log the exception
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
    handler: ListUsersHandler,  # Inject the query handler
    # Use FastAPI's Depends for query parameters to automatically map to ListUsersQuery
    query_params: ListUsersQuery = Depends(),
):
    """
    Retrieves a list of users, potentially with filtering and pagination.
    """
    try:
        # FastAPI automatically creates ListUsersQuery from query params due to Depends()
        user_dtos = await handler.handle(query_params)
        return user_dtos
    except Exception as e:
        print(f"Error listing users: {e}")
        # Log the exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing users.",
        )


# Add other endpoints for update, delete (likely command-based via MQ or direct handlers)
