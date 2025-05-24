import json

from aio_pika.abc import AbstractRobustChannel

from contexts.inventory.application.commands import (
    CreateCollectionCommand,
    CreateItemCommand,
    UpdateCollectionCommand,
    UpdateItemCommand,
    DeleteCollectionCommand,
    DeleteItemCommand,
)
from core.messaging import publish_message

# Configuration
INVENTORY_COMMAND_EXCHANGE = "inventory_commands_exchange"
CREATE_ITEM_ROUTING_KEY = "inventory.command.create"
CREATE_COLLECTION_ROUTING_KEY = "inventory.command.create_collection"
UPDATE_ITEM_ROUTING_KEY = "inventory.command.update"
UPDATE_COLLECTION_ROUTING_KEY = "inventory.command.update_collection"
DELETE_ITEM_ROUTING_KEY = "inventory.command.delete"
DELETE_COLLECTION_ROUTING_KEY = "inventory.command.delete_collection"


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

    async def publish_update_item(self, cmd: UpdateItemCommand):
        """Publish an UpdateItemCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=UPDATE_ITEM_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )

    async def publish_update_collection(self, cmd: UpdateCollectionCommand):
        """Publish an UpdateCollectionCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=UPDATE_COLLECTION_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )

    async def publish_delete_item(self, cmd: DeleteItemCommand):
        """Publish a DeleteItemCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=DELETE_ITEM_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )

    async def publish_delete_collection(self, cmd: DeleteCollectionCommand):
        """Publish a DeleteCollectionCommand."""
        body = cmd.model_dump_json().encode("utf-8")
        await publish_message(
            channel=self.channel,
            exchange_name=INVENTORY_COMMAND_EXCHANGE,
            routing_key=DELETE_COLLECTION_ROUTING_KEY,
            body=body,
            content_type="application/json",
        )