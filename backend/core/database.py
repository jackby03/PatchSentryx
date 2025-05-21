from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Create the async engine
# Use echo=True to log SQL statements (useful for debugging)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # Log SQL only in development
    pool_pre_ping=True,  # Helps detect disconnected connections
)

# Create an async session factory
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,  # Important for async usage
    class_=AsyncSession,
)


# Base class for declarative models
class Base(DeclarativeBase):
    pass


# Dependency to get a database session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an AsyncSession for a request.
    Ensures the session is closed afterwards.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            # Optionally commit here if you want auto-commit behavior,
            # but explicit commits in repositories are generally preferred.
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Alternative context manager usage (often used within repositories)
@asynccontextmanager
async def db_session_manager() -> AsyncGenerator[AsyncSession, None]:
    """Provides a session outside of FastAPI dependency injection."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()  # Commit on successful exit
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize the database.
    Optionally create tables if they don't exist (useful for development/testing).
    """
    # In a production scenario, you'd typically use Alembic migrations.
    # This is a simplified setup.
    # async with engine.begin() as conn:
    #     # await conn.run_sync(Base.metadata.drop_all) # Use with caution!
    #     await conn.run_sync(Base.metadata.create_all)
    print("Database connection initialized.")
    # Check connection (optional)
    try:
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")


async def close_db():
    """Close the database engine connections."""
    await engine.dispose()
    print("Database connections closed.")
