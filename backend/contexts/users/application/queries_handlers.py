import uuid
from typing import List, Optional

from contexts.users.application.queries import (GetUserByIdQuery,
                                                ListUsersQuery, UserDTO)
from contexts.users.domain.repositories import UserRepository
from core.errors import EntityNotFoundError


class GetUserByIdQueryHandler:
    """Handles the GetUserByIdQuery."""

    def __init__(self, user_repository: UserRepository):
        # Note: For pure CQRS, this might use a dedicated Read Model Repository
        # that queries a potentially denormalized read database/table directly.
        # For simplicity here, we reuse the domain repository.
        self.user_repository = user_repository

    async def handle(self, query: GetUserByIdQuery) -> Optional[UserDTO]:
        """
        Executes the query to retrieve a user by ID.

        Returns:
            UserDTO or None if the user is not found.
        """
        print(f"Handling GetUserByIdQuery for ID: {query.user_id}")
        user = await self.user_repository.get_by_id(query.user_id)
        if not user:
            # Raise EntityNotFoundError here if the API should return 404
            # Or return None if the caller/API handles the None case
            # raise EntityNotFoundError("User", query.user_id)
            print(f"User with ID {query.user_id} not found.")
            return None

        # Map the domain entity to the DTO
        return UserDTO.model_validate(user)


class ListUsersQueryHandler:
    """Handles the ListUsersQuery."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, query: ListUsersQuery) -> List[UserDTO]:
        """
        Executes the query to retrieve a list of users.
        (Note: Filtering/pagination logic would be added here or in the repository)
        """
        print(
            f"Handling ListUsersQuery with limit={query.limit}, offset={query.offset}"
        )
        # Basic implementation: List all users (modify repository or add logic here for filters/pagination)
        users = await self.user_repository.list_all()  # This needs pagination/filtering

        # Filter based on query parameters (example)
        filtered_users = users
        if query.is_active is not None:
            filtered_users = [u for u in users if u.is_active == query.is_active]

        # Apply pagination (simple slicing example)
        paginated_users = filtered_users[query.offset : query.offset + query.limit]

        # Map domain entities to DTOs
        return [UserDTO.model_validate(user) for user in paginated_users]


# --- Add other query handlers here ---
