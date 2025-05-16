from typing import Annotated

from fastapi import Depends

from contexts.users.application.command_handlers import \
    CreateUserCommandHandler
from contexts.users.application.queries_handlers import (
    GetUserByIdQueryHandler, ListUsersQueryHandler)
from contexts.users.domain.repositories import UserRepository
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.dependencies import DbSession


def get_user_repository(session: DbSession) -> UserRepository:
    return SQLAlchemyUserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]


def get_create_user_command_handler(repo: UserRepo) -> CreateUserCommandHandler:
    return CreateUserCommandHandler(user_repository=repo)


CreateUserHandler = Annotated[
    CreateUserCommandHandler, Depends(get_create_user_command_handler)
]


def get_user_by_id_query_handler(repo: UserRepo) -> GetUserByIdQueryHandler:
    return GetUserByIdQueryHandler(user_repository=repo)


GetUserByIdHandler = Annotated[
    GetUserByIdQueryHandler, Depends(get_user_by_id_query_handler)
]


def get_list_users_query_handler(repo: UserRepo) -> ListUsersQueryHandler:
    return ListUsersQueryHandler(user_repository=repo)


ListUsersHandler = Annotated[
    ListUsersQueryHandler, Depends(get_list_users_query_handler)
]
