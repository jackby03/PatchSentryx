from contexts.inventory.application.commands import (
    CreateItemCommand,
    UpdateItemCommand,
    DeleteItemCommand,
    CreateCollectionCommand,
    UpdateCollectionCommand,
    DeleteCollectionCommand,
)
from contexts.inventory.domain.entities import Item, Collection
from contexts.inventory.infrastructure.repositories import InventoryRepository


# --- Item Commands ---
class CreateItemCommandHandler:
    """Handles the CreateItemCommand."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, command: CreateItemCommand) -> Item:
        print(f"Handling CreateItemCommand for {command.name}")
        item = Item(
            name=command.name,
            hostname=command.hostname,
            version=command.version,
            brand=command.brand,
            model=command.model,
            serial_number=command.serial_number,
            location=command.location,
        )
        await self.repository.add_item(item)
        print(f"Created item {item.id} successfully.")
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


# --- Collection Commands ---


class CreateCollectionCommandHandler:
    """Handles the CreateCollectionCommand."""

    def __init__(self, repository: InventoryRepository):
        """
        Initializes the handler with the repository.

        Args:
            repository: An instance of InventoryRepository.
        """
        self.repository = repository

    async def handle(self, command: CreateCollectionCommand) -> Collection:
        """
        Handles the creation of a new Collection.

        Args:
            command: The CreateCollectionCommand containing the data to create a Collection.

        Returns:
            The created Collection.
        """
        print(f"Handling CreateCollectionCommand for {command.name}")
        collection = Collection(
            name=command.name,
            description=command.description,
            items=[],
        )
        await self.repository.add_collection(collection)
        print(f"Created collection {collection.id} successfully.")
        return collection


class UpdateCollectionCommandHandler:
    """Handles the UpdateCollectionCommand."""

    def __init__(self, repository: InventoryRepository):
        """
        Initializes the handler with the repository.

        Args:
            repository: An instance of InventoryRepository.
        """
        self.repository = repository

    async def handle(self, command: UpdateCollectionCommand) -> Collection:
        """
        Handles the update of an existing Collection.

        Args:
            command: The UpdateCollectionCommand containing the data to update the Collection.

        Returns:
            The updated Collection.

        Raises:
            Exception: If the Collection with the given ID is not found.
        """
        print(f"Handling UpdateCollectionCommand for {command.id}")

        # Fetch the existing collection
        collection = await self.repository.get_collection_by_id(command.id)
        if not collection:
            raise Exception(f"Collection with ID {command.id} not found.")

        # Update attributes
        if command.name is not None:
            collection.name = command.name
        if command.description is not None:
            collection.description = command.description
        if command.items is not None:
            collection.items = command.items

        # Persist the changes
        await self.repository.update_collection(collection)
        print(f"Updated collection {collection.id} successfully.")
        return collection


class DeleteCollectionCommandHandler:
    """Handles the DeleteCollectionCommand."""

    def __init__(self, repository: InventoryRepository):
        """
        Initializes the handler with the repository.

        Args:
            repository: An instance of InventoryRepository.
        """
        self.repository = repository

    async def handle(self, command: DeleteCollectionCommand) -> None:
        """
        Handles the deletion of an existing Collection.

        Args:
            command: The DeleteCollectionCommand containing the ID of the Collection to delete.

        Raises:
            Exception: If the Collection with the given ID is not found.
        """
        print(f"Handling DeleteCollectionCommand for {command.id}")

        # Fetch the existing collection to ensure it exists
        collection = await self.repository.get_collection_by_id(command.id)
        if not collection:
            raise Exception(f"Collection with ID {command.id} not found.")

        # Delete the collection from the repository
        await self.repository.delete_collection(command.id)
        print(f"Deleted collection {command.id} successfully.")
