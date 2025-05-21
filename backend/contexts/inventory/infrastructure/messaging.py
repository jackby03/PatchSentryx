import json

from aio_pika.abc import AbstractRobustChannel

from contexts.inventory.application.commands import (
    CreateCollectionCommand,
    CreateItemCommand,
)
from core.messaging import publish_message

# Configuration
INVENTORY_COMMAND_EXCHANGE = "inventory_commands_exchange"
CREATE_ITEM_ROUTING_KEY = "inventory.command.create"
CREATE_COLLECTION_ROUTING_KEY = "inventory.command.create_collection"


class InventoryCommandPublisher:
    """Publishes inventory-related commands to RabbitMQ."""

    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    async def publish_create_item(self, cmd: CreateItemCommand):
        """Publish a CreateItemCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=CREATE_ITEM_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )

    async def publish_create_collection(self, cmd: CreateCollectionCommand):
        """Publish a CreateCollectionCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=CREATE_COLLECTION_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )
