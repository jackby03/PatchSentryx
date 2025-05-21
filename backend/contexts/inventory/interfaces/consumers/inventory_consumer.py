import asyncio
import json
import os
import sys

from aio_pika.abc import AbstractIncomingMessage

from contexts.inventory.application.command_handlers import CreateItemCommandHandler

# Application imports
from contexts.inventory.application.commands import CreateItemCommand
from contexts.inventory.infrastructure.repositories import SQLAlchemyInventoryRepository
from core.database import AsyncSessionFactory, close_db
from core.errors import DomainError
from core.messaging import get_rabbitmq_connection, setup_messaging_infrastructure

# Add project root to path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
sys.path.insert(0, project_root)

# Messaging configuration
INVENTORY_COMMAND_EXCHANGE = "inventory_commands_exchange"
CREATE_ITEM_QUEUE = "create_item_queue"
CREATE_ITEM_ROUTING_KEY = "inventory.command.create"


async def process_create_item_message(message: AbstractIncomingMessage):
    async with message.process(ignore_processed=True):
        payload = message.body.decode()
        print(f"[InventoryConsumer] Received: {payload}")
        try:
            data = json.loads(payload)
            cmd = CreateItemCommand(**data)

            async with AsyncSessionFactory() as session:
                repo = SQLAlchemyInventoryRepository(session)
                handler = CreateItemCommandHandler(repo)
                await handler.handle(cmd)
                await session.commit()
                await message.ack()
                print(f"[InventoryConsumer] Created item '{cmd.name}'")

        except DomainError as de:
            print(f"[InventoryConsumer] DomainError: {de}, rejecting")
            await message.reject(requeue=False)
        except Exception as e:
            print(f"[InventoryConsumer] Error: {e}, nacking")
            await message.nack(requeue=False)
            raise


async def consume_inventory_commands():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    await setup_messaging_infrastructure(channel)
    queue = await channel.get_queue(CREATE_ITEM_QUEUE)
    await queue.consume(process_create_item_message)
    print("[InventoryConsumer] Waiting for messages. CTRL+C to exit")
    await asyncio.Event().wait()


if __name__ == "__main__":
    print("Starting Inventory Consumer...")
    try:
        asyncio.run(consume_inventory_commands())
    except KeyboardInterrupt:
        print("Inventory Consumer: interrupted")
    finally:
        asyncio.run(close_db())
