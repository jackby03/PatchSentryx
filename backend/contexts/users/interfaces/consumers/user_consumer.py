import asyncio
import json
import os
import sys
from typing import Optional

# Add project root to path to allow imports when run directly
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
sys.path.insert(0, project_root)


from aio_pika.abc import AbstractIncomingMessage

from contexts.users.application.command_handlers import \
    CreateUserCommandHandler
from contexts.users.application.commands import CreateUserCommand
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.database import (  # Import session factory and closer
    AsyncSessionFactory, close_db)
from core.errors import DomainError
from core.messaging import close_rabbitmq_connection  # Import MQ utils
from core.messaging import (get_rabbitmq_connection,
                            setup_messaging_infrastructure)

# Configuration
USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_QUEUE = "create_user_queue"
CREATE_USER_ROUTING_KEY = "user.command.create"


async def process_create_user_message(message: AbstractIncomingMessage):
    """Processes a message from the create_user_queue."""
    async with message.process(
        ignore_processed=True
    ):  # Use ignore_processed for potential redelivery on failure before ack
        print(f"Received message: {message.body.decode()}")

        try:
            # Decode message body
            data = json.loads(message.body.decode())
            command = CreateUserCommand(**data)

            # Get dependencies (Database Session, Repository, Handler)
            # We need a new DB session for each message
            async with AsyncSessionFactory() as session:
                try:
                    repo = SQLAlchemyUserRepository(session)
                    handler = CreateUserCommandHandler(user_repository=repo)

                    print(f"Consumer: Handling create user command for {command.email}")
                    await handler.handle(command)
                    await session.commit()  # Commit the transaction for this message
                    print(
                        f"Consumer: Successfully processed create user command for {command.email}"
                    )
                    await (
                        message.ack()
                    )  # Acknowledge message only after successful processing and commit
                    print("Consumer: Message acknowledged.")

                except DomainError as e:
                    # Handle specific domain errors (e.g., duplicate email)
                    print(
                        f"Consumer: Domain error processing message for {command.email}: {e}. Rejecting message."
                    )
                    # Reject message (and don't requeue, as it's a permanent domain error)
                    await message.reject(requeue=False)
                except Exception as e:
                    # Handle unexpected errors during processing
                    print(
                        f"Consumer: Unexpected error processing message: {e}. Rolling back and nacking."
                    )
                    await session.rollback()
                    # Negative acknowledge, potentially requeue depending on error type
                    # Be careful with requeueing to avoid infinite loops for persistent errors
                    await message.nack(
                        requeue=False
                    )  # Consider requeue=True for transient errors
                    raise  # Re-raise to log or handle upstream if needed

        except json.JSONDecodeError:
            print("Consumer: Failed to decode JSON message body. Rejecting.")
            await message.reject(requeue=False)  # Invalid message, don't requeue
        except Exception as e:
            # Handle errors during initial message parsing or connection issues
            print(f"Consumer: Error before processing started: {e}. Nacking.")
            await message.nack(
                requeue=False
            )  # Don't requeue if message structure is bad
            raise  # Re-raise to potentially stop the consumer


async def consume_create_user_commands():
    """Sets up and runs the consumer for the create_user_queue."""
    connection = None
    channel = None
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)  # Process one message at a time

        # Ensure queue and bindings exist (idempotent)
        await setup_messaging_infrastructure(channel)

        queue = await channel.get_queue(CREATE_USER_QUEUE)
        print(f"Consumer: Starting consumption from queue '{CREATE_USER_QUEUE}'...")

        # Start consuming
        await queue.consume(process_create_user_message)

        print("Consumer: Waiting for messages. To exit press CTRL+C")
        # Keep the consumer running indefinitely
        await asyncio.Event().wait()

    except asyncio.CancelledError:
        print("Consumer: Consumption cancelled.")
    except Exception as e:
        print(f"Consumer: An unexpected error occurred: {e}")
    finally:
        print("Consumer: Shutting down...")
        if channel and not channel.is_closed:
            await channel.close()
        # Don't close the global connection here if other parts of the app use it
        # await close_rabbitmq_connection()
        await close_db()  # Close database pool
        print("Consumer: Shutdown complete.")


# Entry point for running the consumer directly
if __name__ == "__main__":
    # Note: Running this directly requires DATABASE_URL and RABBITMQ_URL
    # to be set in the environment or via a .env file loaded by config.py
    # You might need to initialize settings explicitly if not running via FastAPI startup
    from app.config import settings

    print(
        f"Starting User Consumer with DB: {settings.DATABASE_URL} and MQ: {settings.RABBITMQ_URL}"
    )

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(consume_create_user_commands())
    except KeyboardInterrupt:
        print("Consumer: Keyboard interrupt received.")
    finally:
        # Perform cleanup if needed, though consume_create_user_commands handles most
        print("Consumer: Event loop closing.")
        # loop.close() # Closing loop might not be necessary depending on context
