# Standard library imports
import asyncio
import json
import os
import sys

# Third-party imports
from aio_pika.abc import AbstractIncomingMessage

# Application imports
from contexts.users.application.command_handlers import CreateUserCommandHandler
from contexts.users.application.commands import CreateUserCommand
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.database import AsyncSessionFactory, close_db
from core.errors import DomainError
from core.messaging import get_rabbitmq_connection, setup_messaging_infrastructure

# Add the project root to sys.path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
sys.path.insert(0, project_root)

# Configuration constants
USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_QUEUE = "create_user_queue"
CREATE_USER_ROUTING_KEY = "user.command.create"


async def process_create_user_message(message: AbstractIncomingMessage):
    """Processes a message from the create_user_queue."""
    async with message.process(ignore_processed=True):
        print(f"Received message: {message.body.decode()}")
        try:
            data = json.loads(message.body.decode())
            command = CreateUserCommand(**data)

            async with AsyncSessionFactory() as session:
                try:
                    repo = SQLAlchemyUserRepository(session)
                    handler = CreateUserCommandHandler(user_repository=repo)

                    print(f"Consumer: Handling create user command for {command.email}")
                    await handler.handle(command)
                    await session.commit()  # Commit the transaction
                    print(
                        f"Consumer: Successfully processed create user command for {command.email}"
                    )
                    await message.ack()  # Acknowledge the message
                    print("Consumer: Message acknowledged.")

                except DomainError as e:
                    print(
                        f"Consumer: Domain error processing message for {command.email}: {e}. Rejecting message."
                    )
                    await session.rollback()
                    await message.reject(requeue=False)
                except Exception as e:
                    print(f"Consumer: Error during processing: {e}")
                    await session.rollback()
                    await message.nack(requeue=False)
                    raise
        except json.JSONDecodeError:
            print("Consumer: Failed to decode JSON message body. Rejecting.")
            await message.reject(requeue=False)
        except Exception as e:
            print(f"Consumer: Unexpected error before processing: {e}. Nacking.")
            await message.nack(requeue=False)
            raise


async def consume_create_user_commands():
    """Sets up and runs the consumer for the create_user_queue."""
    connection = None
    channel = None
    try:
        print("[DEBUG] Connecting to RabbitMQ...")
        connection = await get_rabbitmq_connection()
        print("[DEBUG] RabbitMQ connection established.")
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        print("[DEBUG] Channel created and QoS set.")

        print("[DEBUG] Setting up messaging infrastructure...")
        await setup_messaging_infrastructure(channel)
        print("[DEBUG] Messaging infrastructure setup complete.")

        queue = await channel.get_queue(CREATE_USER_QUEUE)
        print(f"[DEBUG] Queue '{CREATE_USER_QUEUE}' acquired.")
        print(f"Consumer: Starting consumption from queue '{CREATE_USER_QUEUE}'...")

        await queue.consume(process_create_user_message)

        print("Consumer: Waiting for messages. To exit press CTRL+C")
        # Changed to handle cancellation more cleanly
        await asyncio.Event().wait()

    except asyncio.CancelledError:
        print("Consumer: Consumption cancelled.")
    except Exception as e:
        print(f"Consumer: An unexpected error occurred: {e}")
    finally:
        print("Consumer: Shutting down...")
        if channel and not channel.is_closed:
            await channel.close()
            print("[DEBUG] RabbitMQ channel closed.")
        if connection and not connection.is_closed:
            await connection.close()  # Properly close the global connection
            print("[DEBUG] RabbitMQ connection closed.")
        await close_db()  # Ensure database pool is closed
        print("Consumer: Shutdown complete.")


# Entry point for running the consumer directly
if __name__ == "__main__":
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
