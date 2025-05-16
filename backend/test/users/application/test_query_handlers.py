import uuid
from unittest.mock import AsyncMock

import pytest

from contexts.users.application.queries import (GetUserByIdQuery,
                                                ListUsersQuery, UserDTO)
from contexts.users.application.queries_handlers import (
    GetUserByIdQueryHandler, ListUsersQueryHandler)
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import EntityNotFoundError  # Import if handler raises this

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked UserRepository."""
    repo = AsyncMock(spec=UserRepository)
    return repo


@pytest.fixture
def sample_user():
    """Fixture for a sample User domain entity."""
    return User(
        id=uuid.uuid4(),
        name="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )


# --- Tests for GetUserByIdQueryHandler ---


async def test_get_user_by_id_handler_success(mock_user_repo, sample_user):
    """Test successfully retrieving a user by ID."""
    # Setup mock repo
    mock_user_repo.get_by_id = AsyncMock(return_value=sample_user)

    handler = GetUserByIdQueryHandler(user_repository=mock_user_repo)
    query = GetUserByIdQuery(user_id=sample_user.id)

    result_dto = await handler.handle(query)

    # Assertions
    mock_user_repo.get_by_id.assert_awaited_once_with(sample_user.id)
    assert isinstance(result_dto, UserDTO)
    assert result_dto.id == sample_user.id
    assert result_dto.name == sample_user.name
    assert result_dto.email == sample_user.email
    assert result_dto.is_active == sample_user.is_active


async def test_get_user_by_id_handler_not_found(mock_user_repo):
    """Test retrieving a user by ID when the user doesn't exist."""
    user_id = uuid.uuid4()
    # Setup mock repo
    mock_user_repo.get_by_id = AsyncMock(return_value=None)

    handler = GetUserByIdQueryHandler(user_repository=mock_user_repo)
    query = GetUserByIdQuery(user_id=user_id)

    # Option 1: Handler returns None
    result_dto = await handler.handle(query)
    assert result_dto is None

    # Option 2: Handler raises EntityNotFoundError (Uncomment if implemented)
    # with pytest.raises(EntityNotFoundError) as excinfo:
    #     await handler.handle(query)
    # assert f"User with ID '{user_id}' not found" in str(excinfo.value)

    mock_user_repo.get_by_id.assert_awaited_once_with(user_id)


# --- Tests for ListUsersQueryHandler ---


@pytest.fixture
def sample_user_list(sample_user):
    """Fixture for a list of sample users."""
    user2 = User(
        id=uuid.uuid4(),
        name="Another User",
        email="another@example.com",
        hashed_password="pw2",
        is_active=False,
    )
    user3 = User(
        id=uuid.uuid4(),
        name="Active User 2",
        email="active2@example.com",
        hashed_password="pw3",
        is_active=True,
    )
    return [sample_user, user2, user3]


async def test_list_users_handler_success_no_filters(mock_user_repo, sample_user_list):
    """Test listing users without filters or pagination."""
    # Setup mock repo
    mock_user_repo.list_all = AsyncMock(return_value=sample_user_list)

    handler = ListUsersQueryHandler(user_repository=mock_user_repo)
    query = ListUsersQuery()  # Default limit/offset

    result_dtos = await handler.handle(query)

    # Assertions
    mock_user_repo.list_all.assert_awaited_once()  # Assumes repo handles pagination/filtering
    assert len(result_dtos) == len(
        sample_user_list
    )  # Check if all returned (before pagination)
    assert all(isinstance(dto, UserDTO) for dto in result_dtos)
    assert result_dtos[0].id == sample_user_list[0].id
    assert result_dtos[1].id == sample_user_list[1].id


async def test_list_users_handler_with_pagination(mock_user_repo, sample_user_list):
    """Test listing users with pagination (limit and offset)."""
    # Setup mock repo to return the full list
    mock_user_repo.list_all = AsyncMock(return_value=sample_user_list)

    handler = ListUsersQueryHandler(user_repository=mock_user_repo)
    # Query for the second page (limit 1, offset 1)
    query = ListUsersQuery(limit=1, offset=1)

    result_dtos = await handler.handle(query)

    # Assertions
    mock_user_repo.list_all.assert_awaited_once()
    assert len(result_dtos) == 1  # Only one user returned due to limit
    assert (
        result_dtos[0].id == sample_user_list[1].id
    )  # The second user in the original list


async def test_list_users_handler_with_filter(mock_user_repo, sample_user_list):
    """Test listing users filtering by active status."""
    # Setup mock repo to return the full list
    mock_user_repo.list_all = AsyncMock(return_value=sample_user_list)
    active_users = [u for u in sample_user_list if u.is_active]

    handler = ListUsersQueryHandler(user_repository=mock_user_repo)
    # Query for only active users
    query = ListUsersQuery(is_active=True)

    result_dtos = await handler.handle(query)

    # Assertions
    mock_user_repo.list_all.assert_awaited_once()
    assert len(result_dtos) == len(active_users)  # Only active users returned
    assert all(dto.is_active for dto in result_dtos)
    assert {dto.id for dto in result_dtos} == {u.id for u in active_users}


async def test_list_users_handler_empty_result(mock_user_repo):
    """Test listing users when the repository returns an empty list."""
    # Setup mock repo
    mock_user_repo.list_all = AsyncMock(return_value=[])

    handler = ListUsersQueryHandler(user_repository=mock_user_repo)
    query = ListUsersQuery()

    result_dtos = await handler.handle(query)

    # Assertions
    mock_user_repo.list_all.assert_awaited_once()
    assert len(result_dtos) == 0
    assert result_dtos == []


# Add tests for more complex filtering/sorting scenarios if implemented.
