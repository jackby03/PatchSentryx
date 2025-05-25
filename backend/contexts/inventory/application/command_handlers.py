from contexts.inventory.application.commands import (
    CreateItemCommand,
    DeleteItemCommand,
    UpdateItemCommand,
)
from contexts.inventory.domain.entities import Item
from contexts.inventory.infrastructure.repositories import InventoryRepository


# --- Item Commands ---
class CreateItemCommandHandler:
    """Handles the CreateItemCommand."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, command: CreateItemCommand) -> Item:
        item = Item(
            name=command.name,
            hostname=command.hostname,
            version=command.version,
            brand=command.brand,
            model=command.model,
            serial_number=command.serial_number,
            location=command.location,
            user_id=command.user_id,
            is_active=command.is_active,
        )
        print(f"Creating item entity: {item}")
        await self.repository.add_item(item)
        print(f"Item created successfully with ID: {item.id}")
        return item


class UpdateItemCommandHandler:
    """Handles the UpdateItemCommand."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, command: UpdateItemCommand) -> Item:
        print(f"Handling UpdateItemCommand for {command.id}")
        item = await self.repository.get_item_by_id(command.id)
        if not item:
            raise Exception(f"Item with ID {command.id} not found.")
        await self.repository.update_item(item)
        print(f"Updated item {item.id} successfully.")
        return item


class DeleteItemCommandHandler:
    """Handles the DeleteItemCommand."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, command: DeleteItemCommand) -> None:
        print(f"Handling DeleteItemCommand for {command.id}")
        item = await self.repository.get_item_by_id(command.id)
        if not item:
            print(f"Item with ID {command.id} not found.")
            return
        await self.repository.delete_item(command.id)
        print(f"Deleted item {item.id} successfully.")
