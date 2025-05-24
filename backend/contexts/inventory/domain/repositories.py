# Standard library imports
import abc
import uuid
from typing import Optional

# Application imports
from contexts.inventory.domain.entities import Collection, Item


class InventoryRepository(abc.ABC):
    """
    Abstract base class for inventory repository.
    Defines the contract for how the application interacts with the inventory data store.
    """

    # CRUD operations for Items

    # Query operations
    @abc.abstractmethod
    async def get_item_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        """Retrieves an inventory item by its ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_all_items(self) -> list[Item]:
        """Lists all inventory items in the repository."""
        raise NotImplementedError

    # Command operations
    @abc.abstractmethod
    async def add_item(self, item: Item) -> None:
        """Adds a new inventory item to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update_item(self, item: Item) -> None:
        """Updates an existing inventory item in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_item(self, item_id: uuid.UUID) -> None:
        """Deletes an inventory item from the repository."""
        raise NotImplementedError

    # CRUD operations for Collections

    # Query operations
    @abc.abstractmethod
    async def get_collection_by_id(
        self, collection_id: uuid.UUID
    ) -> Optional[Collection]:
        """Retrieves a collection by its ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_all_collections(self) -> list[Collection]:
        """Lists all collections in the repository."""
        raise NotImplementedError

    # Command operations
    @abc.abstractmethod
    async def add_collection(self, collection: Collection) -> None:
        """Adds a new collection to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update_collection(self, collection: Collection) -> None:
        """Updates an existing collection in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_collection(self, collection_id: uuid.UUID) -> None:
        """Deletes a collection from the repository, optionally deleting its items."""
        raise NotImplementedError

    # Additional operations
    @abc.abstractmethod
    async def get_items_by_collection_id(self, collection_id: uuid.UUID) -> list[Item]:
        """Retrieves all items belonging to a specific collection."""
        raise NotImplementedError

    @abc.abstractmethod
    async def search_items(self, query: str) -> list[Item]:
        """Searches for items based on a query string."""
        raise NotImplementedError

    @abc.abstractmethod
    async def count_items(self, is_active: Optional[bool] = None) -> int:
        """Counts the number of items, optionally filtering by active status."""
        raise NotImplementedError
