from sqlalchemy.ext.asyncio import AsyncSession

from contexts.users.application.command_handlers import CreateUserCommandHandler
from contexts.users.application.queries_handlers import (
    GetUserByIdQueryHandler,
    ListUsersQueryHandler,
)

# from core.messaging import get_rabbitmq_connection # If getting connection centrally
from contexts.users.domain.repositories import UserRepository
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.database import AsyncSessionFactory  # Get the factory

# from aio_pika.abc import AbstractRobustChannel # If managing MQ channel centrally


# Import other handlers and repositories


class Container:
    """Simple DI Container Example"""

    # You could initialize external connections here if needed,
    # but managing session/channel lifecycle per request/task is often better.
    # db_session_factory = AsyncSessionFactory
    # mq_connection_factory = get_rabbitmq_connection

    @staticmethod
    def get_user_repository(session: AsyncSession) -> UserRepository:
        # Factory method for UserRepository
        return SQLAlchemyUserRepository(session)

    # --- Command Handlers ---
    @classmethod
    def get_create_user_handler(cls, session: AsyncSession) -> CreateUserCommandHandler:
        repo = cls.get_user_repository(session)
        return CreateUserCommandHandler(user_repository=repo)

    # --- Query Handlers ---
    @classmethod
    def get_user_by_id_handler(cls, session: AsyncSession) -> GetUserByIdQueryHandler:
        repo = cls.get_user_repository(session)
        return GetUserByIdQueryHandler(user_repository=repo)

    @classmethod
    def get_list_users_handler(cls, session: AsyncSession) -> ListUsersQueryHandler:
        repo = cls.get_user_repository(session)
        return ListUsersQueryHandler(user_repository=repo)


# How to use this (example in a consumer or background task):
#
# async def some_background_task():
#     async with AsyncSessionFactory() as session:
#         # Manually resolve dependencies using the container
#         create_user_handler = Container.get_create_user_handler(session)
#         # ... use the handler ...
#         await session.commit() # Remember to commit/rollback


# NOTE: For FastAPI endpoints, using `Depends` as shown in the
# `interfaces/dependencies.py` files is generally the more idiomatic and simpler approach.
# This container example is more relevant if you have complex dependency graphs outside
# the FastAPI request lifecycle or prefer this explicit style.
