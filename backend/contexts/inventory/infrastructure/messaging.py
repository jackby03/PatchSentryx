from aio_pika.abc import AbstractRobustChannel

from contexts.inventory.application.commands import (
    CreateItemCommand,
    DeleteItemCommand,
    UpdateItemCommand,
)
from core.messaging import publish_message

# Configuration
INVENTORY_COMMAND_EXCHANGE = "inventory_commands_exchange"
CREATE_ITEM_ROUTING_KEY = "inventory.command.create"
UPDATE_ITEM_ROUTING_KEY = "inventory.command.update"
DELETE_ITEM_ROUTING_KEY = "inventory.command.delete"


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
