import uuid
from unittest.mock import \
    ANY  # For asserting mock calls with generated IDs etc.

import pytest
from httpx import AsyncClient

from contexts.users.application.commands import \
    CreateUserCommand  # For payload structure
from contexts.users.domain.entities import User  # For checking repo calls
from core.security import get_password_hash  # For creating test users directly

pytestmark = pytest.mark.asyncio

# --- Fixtures ---


@pytest.fixture
def user_create_payload():
    """Payload for creating a new user via API."""
    return {
        "name": "API Test User",
        "email": "api.test@example.com",
        "password": "password123",
    }


@pytest.fixture
async def existing_user(db_session) -> User:
    """Creates a user directly in the DB for testing GET/update/delete."""
    user = User(
        id=uuid.uuid4(),
        name="Existing User",
        email="existing@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=True,
    )
    # Map to model and add (assuming mappers exist or done manually)
    from contexts.users.infrastructure.models import UserModel

    user_model = UserModel(
        id=user.id,
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
    )
    db_session.add(user_model)
    await db_session.commit()  # Commit directly in fixture for test setup
    await db_session.refresh(user_model)  # Refresh to get committed state if needed
    # Return the domain entity for convenience in tests
    return user


# --- Test Cases ---


# Test POST /users/ (Command Publishing Endpoint)
async def test_register_user_command_success(
    test_client: AsyncClient, mock_rabbitmq_channel, user_create_payload
):
    """Test successful user registration command publishing."""

    response = await test_client.post("/users/", json=user_create_payload)

    # Assertions
    assert response.status_code == 202  # Accepted
    assert response.json()["message"] == "User creation request accepted."
    assert response.json()["email"] == user_create_payload["email"]

    # Check if RabbitMQ publish was called correctly
    mock_rabbitmq_channel.assert_awaited_once()
    # Inspect the arguments passed to the mock publish call
    call_args, _ = mock_rabbitmq_channel.call_args
    published_command = CreateUserCommand.model_validate_json(
        call_args[0].body.decode()
    )  # Assuming first arg is the message obj
    assert published_command.name == user_create_payload["name"]
    assert published_command.email == user_create_payload["email"]
    assert published_command.password == user_create_payload["password"]


async def test_register_user_command_invalid_payload(
    test_client: AsyncClient, mock_rabbitmq_channel
):
    """Test user registration command publishing with invalid data (e.g., bad email)."""
    invalid_payload = {
        "name": "API Test User",
        "email": "invalid-email",  # Invalid email
        "password": "password123",
    }
    response = await test_client.post("/users/", json=invalid_payload)

    # Assertions
    assert response.status_code == 422  # Unprocessable Entity (FastAPI validation)
    mock_rabbitmq_channel.assert_not_awaited()  # Publish should not be called


async def test_register_user_command_missing_field(
    test_client: AsyncClient, mock_rabbitmq_channel
):
    """Test user registration command publishing with missing required field."""
    invalid_payload = {
        "name": "API Test User",
        "password": "password123",
        # Email is missing
    }
    response = await test_client.post("/users/", json=invalid_payload)
    assert response.status_code == 422  # Unprocessable Entity
    mock_rabbitmq_channel.assert_not_awaited()


# Test GET /users/{user_id}
async def test_get_user_success(test_client: AsyncClient, existing_user: User):
    """Test successfully getting an existing user by ID."""
    response = await test_client.get(f"/users/{existing_user.id}")

    # Assertions
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["id"] == str(existing_user.id)
    assert user_data["name"] == existing_user.name
    assert user_data["email"] == existing_user.email
    assert user_data["is_active"] == existing_user.is_active


async def test_get_user_not_found(test_client: AsyncClient):
    """Test getting a user that does not exist."""
    non_existent_id = uuid.uuid4()
    response = await test_client.get(f"/users/{non_existent_id}")

    # Assertions
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_get_user_invalid_uuid(test_client: AsyncClient):
    """Test getting a user with an invalid UUID format."""
    invalid_id = "not-a-uuid"
    response = await test_client.get(f"/users/{invalid_id}")
    assert response.status_code == 422  # FastAPI validation


# Test GET /users/
async def test_list_users_success(test_client: AsyncClient, existing_user: User):
    """Test listing users successfully."""
    # Create another user for the list
    user2 = User(
        id=uuid.uuid4(),
        name="List User 2",
        email="list2@example.com",
        hashed_password=get_password_hash("pw2"),
    )
    from contexts.users.infrastructure.models import UserModel
    from contexts.users.infrastructure.repositories import _map_entity_to_model

    async with test_client.app.state.db_session_manager() as session:  # Get session from app state if needed or use fixture
        session.add(_map_entity_to_model(user2))
        await session.commit()

    response = await test_client.get("/users/")

    # Assertions
    assert response.status_code == 200
    users_list = response.json()
    assert isinstance(users_list, list)
    # Check if both users are present (order might vary)
    user_ids = {user["id"] for user in users_list}
    assert str(existing_user.id) in user_ids
    assert str(user2.id) in user_ids
    # Add more specific checks if needed (filtering, pagination)


async def test_list_users_with_params(test_client: AsyncClient, existing_user: User):
    """Test listing users with query parameters (e.g., limit, offset, filter)."""
    # Example: Get only 1 user
    response = await test_client.get("/users/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Example: Filter by active status (assuming existing_user is active)
    response = await test_client.get("/users/?is_active=true")
    assert response.status_code == 200
    active_user_ids = {user["id"] for user in response.json()}
    assert str(existing_user.id) in active_user_ids

    response = await test_client.get("/users/?is_active=false")
    assert response.status_code == 200
    inactive_user_ids = {user["id"] for user in response.json()}
    assert str(existing_user.id) not in inactive_user_ids


# Add tests for other endpoints (PUT, DELETE) if implemented,
# considering whether they use direct handlers or command publishing.
# If using command publishing, tests would be similar to test_register_user_command_success,
# checking the published message.
# If using direct handlers, tests would check the database state changes.
