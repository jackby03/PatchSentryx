import asyncio
import json
import os
import sys

from aio_pika.abc import AbstractIncomingMessage

from contexts.inventory.application.command_handlers import (
    CreateItemCommandHandler,
    DeleteItemCommandHandler,
    UpdateItemCommandHandler,
)
from contexts.inventory.application.commands import (
    CreateItemCommand,
    DeleteItemCommand,
    UpdateItemCommand,
)
from contexts.inventory.infrastructure.repositories import SQLAlchemyInventoryRepository
from core.database import AsyncSessionFactory, close_db
from core.errors import DomainError
from core.messaging import get_rabbitmq_connection, setup_messaging_infrastructure

# Add a project root to a path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
sys.path.insert(0, project_root)

# Messaging configuration
INVENTORY_COMMAND_EXCHANGE = "inventory_commands_exchange"

# Queue and routing key mapping for each command type
COMMAND_CONFIG = {
    "create_item": {
        "queue": "create_item_queue",
        "routing_key": "inventory.command.create",
        "command_cls": CreateItemCommand,
        "handler_cls": CreateItemCommandHandler,
        "entity": "item",
        "operation": "Created",
    },
    "update_item": {
        "queue": "update_item_queue",
        "routing_key": "inventory.command.update",
        "command_cls": UpdateItemCommand,
        "handler_cls": UpdateItemCommandHandler,
        "entity": "item",
        "operation": "Updated",
    },
    "delete_item": {
        "queue": "delete_item_queue",
        "routing_key": "inventory.command.delete",
        "command_cls": DeleteItemCommand,
        "handler_cls": DeleteItemCommandHandler,
        "entity": "item",
        "operation": "Deleted",
    },
}


def get_handler_config_by_queue(queue_name: str):
    for config in COMMAND_CONFIG.values():
        if config["queue"] == queue_name:
            return config
    return None


def create_message_processor(config):
    async def process_message(message: AbstractIncomingMessage):
        async with message.process(ignore_processed=True):
            payload = message.body.decode()
            print(f"[InventoryConsumer] Received: {payload}")
            try:
                data = json.loads(payload)
                cmd = config["command_cls"](**data)
                print(
                    f"[InventoryConsumer] Handling {config['operation'].lower()} {config['entity']} command"
                )
                async with AsyncSessionFactory() as session:
                    repo = SQLAlchemyInventoryRepository(session)
                    handler = config["handler_cls"](repo)
                    await handler.handle(cmd)
                    await session.commit()
                    await message.ack()
                    print(
                        f"[InventoryConsumer] {config['operation']} {config['entity']} (id: {getattr(cmd, 'id', None)})"
                    )

            except DomainError as de:
                print(f"[InventoryConsumer] DomainError: {de}, rejecting")
                await message.reject(requeue=False)
            except Exception as e:
                print(f"[InventoryConsumer] Error: {e}, nacking")
                await message.nack(requeue=False)
                raise

    return process_message


async def consume_inventory_commands():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    await setup_messaging_infrastructure(channel)

    # Create all queues and consumers for commands
    for cmd_name, config in COMMAND_CONFIG.items():
        queue = await channel.get_queue(config["queue"])
        processor = create_message_processor(config)
        await queue.consume(processor)
        print(
            f"[InventoryConsumer] Listening on {config['queue']} for {config['entity']} {cmd_name.split('_')[0]} commands"
        )

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
