import uuid
from unittest.mock import AsyncMock

import pytest

from contexts.auth.application.authenticate_user import (
    AuthenticateUserRequest,
    AuthenticateUserUseCase,
)
from contexts.auth.domain.entities import Token
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import AuthorizationError, EntityNotFoundError
from core.security import create_access_token  # For setting up user
from core.security import get_password_hash

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_user_repo():
    """Fixture for a mocked UserRepository."""
    repo = AsyncMock(spec=UserRepository)
    return repo


@pytest.fixture
def test_user() -> User:
    """Fixture for a valid test user entity."""
    password = "password123"
    user = User(
        id=uuid.uuid4(),
        name="Test User",
        email="test@example.com",
        hashed_password=get_password_hash(password),  # Store hashed password
        is_active=True,
    )
    # Attach plain password for verification in tests if needed, but not stored on entity
    user._plain_password = password  # Non-standard, just for test convenience
    return user


@pytest.fixture
def auth_request(test_user) -> AuthenticateUserRequest:
    """Fixture for a valid AuthenticateUserRequest matching the test_user."""
    return AuthenticateUserRequest(
        username=test_user.email,
        password=test_user._plain_password,  # Use the plain password
    )


async def test_authenticate_user_success(mock_user_repo, test_user, auth_request):
    """Test successful user authentication."""
    # Setup mock repo to return the test user
    mock_user_repo.get_by_email = AsyncMock(return_value=test_user)

    use_case = AuthenticateUserUseCase(user_repository=mock_user_repo)
    result_token = await use_case.execute(auth_request)

    # Assertions
    mock_user_repo.get_by_email.assert_awaited_once_with(auth_request.username)
    assert isinstance(result_token, Token)
    assert result_token.token_type == "bearer"
    assert isinstance(result_token.access_token, str)
    assert len(result_token.access_token) > 10  # Basic check for token format

    # Optionally decode token to check payload (requires SECRET_KEY access)
    from core.security import decode_access_token

    payload = decode_access_token(result_token.access_token)
    assert payload is not None
    assert payload.get("sub") == str(test_user.id)
    assert payload.get("email") == test_user.email


async def test_authenticate_user_not_found(mock_user_repo, auth_request):
    """Test authentication fails when user email is not found."""
    # Setup mock repo to return None
    mock_user_repo.get_by_email = AsyncMock(return_value=None)

    use_case = AuthenticateUserUseCase(user_repository=mock_user_repo)

    # Assertions
    with pytest.raises(AuthorizationError) as excinfo:  # Expect generic auth error
        await use_case.execute(auth_request)

    # Check if the specific message is raised (depends on implementation)
    assert "Incorrect username or password" in str(excinfo.value)
    mock_user_repo.get_by_email.assert_awaited_once_with(auth_request.username)


async def test_authenticate_user_incorrect_password(
    mock_user_repo, test_user, auth_request
):
    """Test authentication fails with incorrect password."""
    # Setup mock repo to return the test user
    mock_user_repo.get_by_email = AsyncMock(return_value=test_user)

    # Modify request with wrong password
    invalid_auth_request = AuthenticateUserRequest(
        username=auth_request.username, password="wrong_password"
    )

    use_case = AuthenticateUserUseCase(user_repository=mock_user_repo)

    # Assertions
    with pytest.raises(AuthorizationError) as excinfo:
        await use_case.execute(invalid_auth_request)

    assert "Incorrect username or password" in str(excinfo.value)
    mock_user_repo.get_by_email.assert_awaited_once_with(auth_request.username)


async def test_authenticate_user_inactive(mock_user_repo, test_user, auth_request):
    """Test authentication fails if the user is inactive."""
    # Make the test user inactive
    test_user.is_active = False
    # Setup mock repo to return the inactive test user
    mock_user_repo.get_by_email = AsyncMock(return_value=test_user)

    use_case = AuthenticateUserUseCase(user_repository=mock_user_repo)

    # Assertions
    with pytest.raises(AuthorizationError) as excinfo:
        await use_case.execute(auth_request)

    assert "User account is inactive" in str(excinfo.value)
    mock_user_repo.get_by_email.assert_awaited_once_with(auth_request.username)
