# Standard library imports
import abc
import uuid
from typing import Optional

# Application imports
from contexts.inventory.domain.entities import Item


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

    # Additional operations

    @abc.abstractmethod
    async def search_items(self, query: str) -> list[Item]:
        """Searches for items based on a query string."""
        raise NotImplementedError

    @abc.abstractmethod
    async def count_items(self, is_active: Optional[bool] = None) -> int:
        """Counts the number of items, optionally filtering by active status."""
        raise NotImplementedError
