import uuid
from unittest.mock import AsyncMock  # Use AsyncMock for async methods
from unittest.mock import MagicMock

import pytest

from contexts.users.application.command_handlers import \
    CreateUserCommandHandler
from contexts.users.application.commands import CreateUserCommand
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import DomainError

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked UserRepository."""
    repo = AsyncMock(spec=UserRepository)
    repo.get_by_email = AsyncMock(return_value=None)  # Default: user does not exist
    repo.add = AsyncMock()  # Mock the add method
    return repo


@pytest.fixture
def create_user_command():
    """Fixture for a valid CreateUserCommand."""
    return CreateUserCommand(
        name="Test User", email="test@example.com", password="valid_password123"
    )


async def test_create_user_handler_success(mock_user_repo, create_user_command):
    """Test successful user creation using the command handler."""
    handler = CreateUserCommandHandler(user_repository=mock_user_repo)

    created_user = await handler.handle(create_user_command)

    # Assertions
    mock_user_repo.get_by_email.assert_awaited_once_with(create_user_command.email)
    mock_user_repo.add.assert_awaited_once()

    # Check the user passed to repo.add
    call_args, _ = mock_user_repo.add.call_args
    user_arg = call_args[0]
    assert isinstance(user_arg, User)
    assert user_arg.email == create_user_command.email
    assert user_arg.name == create_user_command.name
    assert user_arg.check_password(
        create_user_command.password
    )  # Verify password was set correctly

    # Check the returned user
    assert created_user == user_arg  # Handler should return the created user


async def test_create_user_handler_email_exists(mock_user_repo, create_user_command):
    """Test user creation fails if email already exists."""
    # Setup mock repo to return an existing user
    existing_user = User(
        id=uuid.uuid4(),
        name="Existing",
        email=create_user_command.email,
        hashed_password="hash",
    )
    mock_user_repo.get_by_email = AsyncMock(return_value=existing_user)

    handler = CreateUserCommandHandler(user_repository=mock_user_repo)

    # Assertions
    with pytest.raises(DomainError) as excinfo:
        await handler.handle(create_user_command)

    assert f"User with email '{create_user_command.email}' already exists." in str(
        excinfo.value
    )
    mock_user_repo.get_by_email.assert_awaited_once_with(create_user_command.email)
    mock_user_repo.add.assert_not_awaited()  # Ensure add was not called


async def test_create_user_handler_repository_error(
    mock_user_repo, create_user_command
):
    """Test handling of repository errors during user creation."""
    # Setup mock repo to raise an error during add
    mock_user_repo.add.side_effect = Exception("Database connection failed")

    handler = CreateUserCommandHandler(user_repository=mock_user_repo)

    # Assertions
    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(create_user_command)

    mock_user_repo.get_by_email.assert_awaited_once_with(create_user_command.email)
    mock_user_repo.add.assert_awaited_once()  # Add was called, but raised error


# Add tests for other command handlers (Update, Delete) following a similar pattern:
# - Mock the repository methods needed by the handler.
# - Set up return values or side effects for the mocks (e.g., user found/not found, errors).
# - Instantiate the handler with the mocked repository.
# - Call the handler's handle method with a command object.
# - Assert that the correct repository methods were called with expected arguments.
# - Assert that the expected exceptions are raised for error cases.
# - Assert the return value of the handler if applicable.
