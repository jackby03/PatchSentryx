import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Ensure ASYNCIO_MODE is set, or pytest-asyncio handles it automatically >= 0.17
# pytestmark = pytest.mark.asyncio


os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://test_user:test_password@127.0.0.1:5433/test_db",
)

os.environ["RABBITMQ_URL"] = os.environ.get(
    "TEST_RABBITMQ_URL", "amqp://guest:guest@localhost:5673/"
)  # Use separate test MQ?

print(f"Database URL: {os.environ['DATABASE_URL']}")
print(f"RabbitMQ URL: {os.environ['RABBITMQ_URL']}")

# Import models from all contexts needed for table creation
from contexts.users.infrastructure.models import UserModel

# --- Database Fixtures ---
# Import Base from your core models or context models
# Ensure all models are imported somewhere before Base.metadata is used
from core.database import Base, get_db_session

# from contexts.auth.infrastructure.models import ... # If auth has models


TEST_DATABASE_URL = os.environ["DATABASE_URL"]


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Overrides pytest default function scoped event loop"""
    # loop = asyncio.get_event_loop_policy().new_event_loop()
    # yield loop
    # loop.close()
    # Simpler approach with pytest-asyncio >= 0.17 (use asyncio_mode = auto)
    # If specific policy needed:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Creates a test database engine scoped for the session."""
    engine = create_async_engine(os.environ["DATABASE_URL"], echo=False)

    try:
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        #     await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        if engine:
            await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a clean database session for each test function.
    Uses transactions for isolation.
    """
    # Connect to the test database
    async with test_engine.connect() as connection:
        # Begin a transaction for the session
        async with connection.begin() as transaction:
            session = async_sessionmaker(
                bind=connection, expire_on_commit=False, class_=AsyncSession
            )()

            try:
                yield session  # Provide the session to the test
            finally:
                # Roll back the transaction and close the session
                await session.close()
                await transaction.rollback()  # Rollback changes after each test
                await connection.close()


# --- Application Fixtures ---
from app.main import app  # Import your FastAPI app instance


@pytest_asyncio.fixture(scope="function")
async def test_client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Creates a test client for making API requests."""

    # Override the database dependency for the test client
    def override_get_db():
        try:
            yield db_session  # Use the function-scoped session
        finally:
            # No need to close here, fixture handles it
            pass

    app.dependency_overrides[get_db_session] = override_get_db  # type: ignore

    # Add overrides for other external dependencies if needed (e.g., RabbitMQ)
    # async def override_get_rabbitmq_channel(): ...
    # app.dependency_overrides[get_rabbitmq_channel] = override_get_rabbitmq_channel

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client

    # Cleanup overrides after a test
    app.dependency_overrides.clear()  # type: ignore


# --- RabbitMQ Fixtures (Optional - more complex setup) ---
# You might want to mock RabbitMQ interactions for unit/integration tests
# or set up a test RabbitMQ instance and provide connection/channel fixtures.


# Example Mocking Fixture (using pytest-mock)
@pytest.fixture
def mock_rabbitmq_channel(mocker):
    # Mock the channel getting function if used directly
    # mock_get_channel = mocker.patch('core.messaging.get_rabbitmq_channel')
    # mock_channel_instance = mocker.AsyncMock(spec=aio_pika.abc.AbstractRobustChannel)
    # mock_get_channel.return_value = ... # Make it return the async context manager

    # Mock the publisher class or specific publish methods
    mock_publisher = mocker.patch(
        "contexts.users.infrastructure.messaging.UserCommandPublisher.publish_create_user_command",
        new_callable=mocker.AsyncMock,
    )
    return mock_publisher


# Add other shared fixtures, factories (using a factory-boy), etc.
