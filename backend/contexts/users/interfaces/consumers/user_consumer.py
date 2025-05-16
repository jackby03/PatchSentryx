import asyncio
import json
import os.path
import sys

from aio_pika.abc import AbstractIncomingMessage

from contexts.users.application.command_handlers import \
    CreateUserCommandHandler
from contexts.users.application.commands import CreateUserCommand
from contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from core.database import AsyncSessionFactory, close_db
from core.errors import DomainError
from core.messaging import (get_rabbitmq_connection,
                            setup_messaing_infrastructure)

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
sys.path.insert(0, project_root)


USER_COMMAND_EXCHANGE = "user_command_exchange"
CREATE_USER_QUEUE = "create_user_queue"
CREATE_USER_ROUTING_KEY = "user.command.create"


async def process_create_user_message(message: AbstractIncomingMessage):
    async with message.process(
        ignore_processed=True,
    ):
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
                    await session.commit()
                    print(f"Consumer: User {command.email} created successfully.")
                    await message.ack()
                    print(f"Consumer: Message acknowledged.")

                except DomainError as e:
                    print(
                        f"Consumer: Domain error processing message for {command.email}: {e}. Rejecting message. "
                    )
                    await message.reject(requeue=False)
                except Exception as e:
                    print(
                        f"Consumer: Error processing message for {command.email}: {e}. Rejecting message."
                    )
                    await session.rollback()
                    await message.nack(requeue=False)
                    raise
        except json.JSONDecodeError as e:
            print(f"Consumer: JSON decode error: {e}. Rejecting message.")
            await message.reject(requeue=False)
        except Exception as e:
            print(f"Consumer: Error processing message: {e}. Rejecting message.")
            await message.nack(requeue=False)
            raise


async def consume_create_user_commands():
    connection = None
    channel = None
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        await setup_messaing_infrastructure(channel)

        queue = await channel.get_queue(CREATE_USER_QUEUE)
        print(f"Consumer: Queue {CREATE_USER_QUEUE} created.")
        await queue.consume(process_create_user_message)
        print("Consumer: Waiting for messages...")
        await asyncio.Event.wait()
    except asyncio.CancelledError:
        print("Consumer: CancelledError. Exiting...")
    except Exception as e:
        print("Consumer: An unexpected error occurred:", e)
    finally:
        print("Consumer: Shutting down...")
        if channel:
            await channel.close()
        await close_db()
        print("Consumer: Shutdown complete.")


if __name__ == "__main__":
    from app.config import settings

    print(
        f"Starting User Consumer with DB: {settings.DATABASE_URL} and MQ: {settings.RABBITMQ_URL}"
    )
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(consume_create_user_commands())
    except KeyboardInterrupt:
        print("Consumer: Keyboard interrupt. Exiting...")
    finally:
        print("consumer: Event loop closing.")
