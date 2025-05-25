from contexts.users.application.commands import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import DomainError, EntityNotFoundError


class CreateUserCommandHandler:
    """Handles the CreateUserCommand."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> User:
        """Executes the command to create a user."""
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
class UpdateUserCommandHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: UpdateUserCommand):
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            raise EntityNotFoundError("User", command.user_id)

        if command.name is not None:
            user.name = command.name
        if command.is_active is not None:
            if command.is_active:
                user.activate()
            else:
                user.deactivate()

        await self.user_repository.update(user)
        print(f"User {user.id} updated.")


class DeleteUserCommandHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: DeleteUserCommand):
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            print(f"User {command.user_id} not found for deletion, skipping.")
            return

        await self.user_repository.delete(command.user_id)
        print(f"User {command.user_id} deleted.")
