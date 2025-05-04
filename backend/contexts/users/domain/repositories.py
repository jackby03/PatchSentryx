import abc
import uuid
from typing import Optional

from contexts.users.domain.entities import User


class UserRepository(abc.ABC):
    """
    Abstract base class for user repository.
    Defines the contract for how the application interacts with the user data store.
    """

    @abc.abstractmethod
    async def add(self, user: User) -> None:
        """Adds a new user to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieves a user by their ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their email."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_all(self) -> list[User]:
        """Lists all users in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, user: User) -> None:
        """Updates an existing user in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, user_id: uuid.UUID) -> None:
        """Deletes a user from the repository."""
        raise NotImplementedError
