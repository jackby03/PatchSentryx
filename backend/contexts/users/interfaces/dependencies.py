from typing import Annotated

from fastapi import Depends

from contexts.users.application.command_handlers import \
    CreateUserCommandHandler  # Import other handlers
from contexts.users.application.queries_handlers import (
    GetUserByIdQueryHandler, ListUsersQueryHandler)
from contexts.users.domain.repositories import UserRepository
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.dependencies import DbSession  # Use the shared DbSession type hint

# --- Repository Dependency ---


def get_user_repository(session: DbSession) -> UserRepository:
    """Dependency provider for UserRepository implementation."""
    return SQLAlchemyUserRepository(session)


# Type hint for user repository dependency
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]


# --- Command Handler Dependencies ---


def get_create_user_command_handler(repo: UserRepo) -> CreateUserCommandHandler:
    """Dependency provider for CreateUserCommandHandler."""
    return CreateUserCommandHandler(user_repository=repo)


# Type hint for Create User command handler dependency
CreateUserHandler = Annotated[
    CreateUserCommandHandler, Depends(get_create_user_command_handler)
]

# Add dependencies for other command handlers here
# def get_update_user_command_handler(...) -> UpdateUserCommandHandler: ...
# UpdateUserHandler = Annotated[UpdateUserCommandHandler, Depends(get_update_user_command_handler)]


# --- Query Handler Dependencies ---


def get_user_by_id_query_handler(repo: UserRepo) -> GetUserByIdQueryHandler:
    """Dependency provider for GetUserByIdQueryHandler."""
    return GetUserByIdQueryHandler(user_repository=repo)


# Type hint for Get User By ID query handler dependency
GetUserByIdHandler = Annotated[
    GetUserByIdQueryHandler, Depends(get_user_by_id_query_handler)
]


def get_list_users_query_handler(repo: UserRepo) -> ListUsersQueryHandler:
    """Dependency provider for ListUsersQueryHandler."""
    return ListUsersQueryHandler(user_repository=repo)


# Type hint for List Users query handler dependency
ListUsersHandler = Annotated[
    ListUsersQueryHandler, Depends(get_list_users_query_handler)
]


# --- Messaging Publisher Dependency (Example) ---
# from core.messaging import get_rabbitmq_channel, Channel
# from contexts.users.infrastructure.messaging import UserCommandPublisher
#
# def get_user_command_publisher(channel: Annotated[Channel, Depends(get_rabbitmq_channel)]) -> UserCommandPublisher:
#     """ Dependency provider for UserCommandPublisher. """
#     return UserCommandPublisher(channel=channel)
#
# UserCmdPublisher = Annotated[UserCommandPublisher, Depends(get_user_command_publisher)]
