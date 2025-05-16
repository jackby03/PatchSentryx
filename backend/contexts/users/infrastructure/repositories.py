import uuid
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from contexts.users.infrastructure.models import UserModel
from core.errors import DatabaseError


# Mapper functions (could be in a separate mappers.py)
def _map_model_to_entity(model: UserModel) -> User:
    """Maps SQLAlchemy UserModel to domain User entity."""
    return User(
        id=model.id,
        name=model.name,
        email=model.email,
        hashed_password=model.hashed_password,
        is_active=model.is_active,
    )


def _map_entity_to_model(
    entity: User, existing_model: Optional[UserModel] = None
) -> UserModel:
    """Maps domain User entity to SQLAlchemy UserModel."""
    if existing_model:
        # Update existing model instance
        existing_model.name = entity.name
        existing_model.email = entity.email
        existing_model.hashed_password = entity.hashed_password
        existing_model.is_active = entity.is_active
        # ID should not change
        return existing_model
    else:
        # Create new model instance
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
        )


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of the UserRepository interface (Adapter).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        """Adds a new user to the database."""
        print(f"SQLAlchemy: Adding user {user.email} to database.")
        user_model = _map_entity_to_model(user)
        try:
            self.session.add(user_model)
            # Flush to ensure ID is generated or handle potential unique constraint errors early
            # Note: commit is often handled by a Unit of Work or the session manager
            await self.session.flush([user_model])
            print(f"SQLAlchemy: Flushed user {user.id}.")
        except Exception as e:
            # Log the error details
            print(f"SQLAlchemy: Error adding user: {e}")
            # Consider specific exception types (e.g., IntegrityError)
            raise DatabaseError(f"Failed to add user: {e}")

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieves a user by their unique ID from the database."""
        print(f"SQLAlchemy: Getting user by ID: {user_id}")
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()

            if user_model:
                return _map_model_to_entity(user_model)
            return None
        except Exception as e:
            print(f"SQLAlchemy: Error getting user by ID: {e}")
            raise DatabaseError(f"Failed to get user by ID: {e}")

    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their email address from the database."""
        print(f"SQLAlchemy: Getting user by email: {email}")
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()

            if user_model:
                return _map_model_to_entity(user_model)
            return None
        except Exception as e:
            print(f"SQLAlchemy: Error getting user by email: {e}")
            raise DatabaseError(f"Failed to get user by email: {e}")

    async def list_all(self) -> List[User]:
        """Retrieves all users from the database. Implement pagination/filtering!"""
        print("SQLAlchemy: Listing all users (Warning: No pagination)")
        try:
            stmt = select(UserModel).order_by(UserModel.name)  # Example ordering
            result = await self.session.execute(stmt)
            user_models = result.scalars().all()
            return [_map_model_to_entity(model) for model in user_models]
        except Exception as e:
            print(f"SQLAlchemy: Error listing users: {e}")
            raise DatabaseError(f"Failed to list users: {e}")

    async def update(self, user: User) -> None:
        """Updates an existing user in the database."""
        print(f"SQLAlchemy: Updating user {user.id}")
        try:
            # Retrieve existing model to update it
            existing_model = await self.session.get(UserModel, user.id)
            if not existing_model:
                # This case might indicate an issue, as update implies existence
                # Or it could be handled as an upsert depending on requirements
                raise DatabaseError(f"User with ID {user.id} not found for update.")

            # Map entity changes onto the existing model
            _map_entity_to_model(user, existing_model)

            # Session automatically tracks changes to existing_model
            await self.session.flush([existing_model])  # Flush changes
            print(f"SQLAlchemy: Flushed updates for user {user.id}.")
        except Exception as e:
            print(f"SQLAlchemy: Error updating user: {e}")
            raise DatabaseError(f"Failed to update user: {e}")

    async def delete(self, user_id: uuid.UUID) -> None:
        """Deletes a user from the database by ID."""
        print(f"SQLAlchemy: Deleting user {user_id}")
        try:
            stmt = delete(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            # Check if any row was actually deleted
            if result.rowcount == 0:
                # Optional: Log or handle the case where the user didn't exist
                print(
                    f"SQLAlchemy: User {user_id} not found for deletion or already deleted."
                )
            else:
                print(
                    f"SQLAlchemy: User {user_id} deleted successfully (rowcount: {result.rowcount})."
                )
            await self.session.flush()  # Ensure deletion is flushed
        except Exception as e:
            print(f"SQLAlchemy: Error deleting user: {e}")
            raise DatabaseError(f"Failed to delete user: {e}")
