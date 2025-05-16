from contexts.users.application.commands import CreateUserCommand
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import DomainError


class CreateUserCommandHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> User:
        print(f"Handling CreateUserCommand for email: {command.email}")
        existing_user = await self.user_repository.get_by_email(command.email)
        if existing_user:
            raise DomainError(f"User with email {command.email} already exists.")
        user = User(
            name=command.name,
            email=command.email,
            hashed_password="",
        )
        user.set_password(command.password)

        await self.user_repository.add(user)
        print(f"User created with id: {user.id}")
        return user
