from contexts.users.application.commands import (
    CreateUserCommand,
)  # Import other commands as needed
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import DomainError  # Use specific errors if needed


class CreateUserCommandHandler:
    """Handles the CreateUserCommand."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> User:
        """
        Executes the command to create a user.

        Raises:
            DomainError: If a user with the given email already exists.
        """
        print(f"Handling CreateUserCommand for email: {command.email}")

        existing_user = await self.user_repository.get_by_email(command.email)
        if existing_user:
            print(f"User {command.email} already exists.")
            raise DomainError(f"User with email '{command.email}' already exists.")
        print(f"Creating user entity for email: {command.email}")
        user = User(
            name=command.name,
            email=command.email,
            hashed_password="",
        )
        user.set_password(command.password)
        print(f"User entity created: {user}")
        await self.user_repository.add(user)
        print(f"User created successfully with ID: {user.id}")

        return user


# --- Add other command handlers here ---

# class UpdateUserCommandHandler:
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
#
#     async def handle(self, command: UpdateUserCommand):
#         user = await self.user_repository.get_by_id(command.user_id)
#         if not user:
#             raise EntityNotFoundError("User", command.user_id)
#
#         # Apply updates...
#         if command.name is not None:
#             user.name = command.name # Assuming direct update or add a method user.change_name()
#         if command.is_active is not None:
#             if command.is_active:
#                 user.activate()
#             else:
#                 user.deactivate()
#
#         await self.user_repository.update(user)
#         print(f"User {user.id} updated.")


# class DeleteUserCommandHandler:
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
#
#     async def handle(self, command: DeleteUserCommand):
#         # Check if user exists first (optional, delete might be idempotent)
#         user = await self.user_repository.get_by_id(command.user_id)
#         if not user:
#             # Decide whether to raise error or silently succeed
#             print(f"User {command.user_id} not found for deletion, skipping.")
#             return
#
#         await self.user_repository.delete(command.user_id)
#         print(f"User {command.user_id} deleted.")
