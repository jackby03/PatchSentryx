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

    # CRUD operations
    @abc.abstractmethod
    async def add_item(self, item: Item) -> None:
        """Adds a new inventory item to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        """Retrieves an inventory item by its ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_all(self) -> list[Item]:
        """Lists all inventory items in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, item: Item) -> None:
        """Updates an existing inventory item in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, item_id: uuid.UUID) -> None:
        """Deletes an inventory item from the repository."""
        raise NotImplementedError

    # Query operations
    @abc.abstractmethod
    async def get_by_name(self, name: str) -> Optional[Item]:
        """Retrieves an inventory item by its name."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_hostname(self, hostname: str) -> Optional[Item]:
        """Retrieves an inventory item by its hostname."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_serial_number(self, serial_number: str) -> Optional[Item]:
        """Retrieves an inventory item by its serial number."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_location(self, location: str) -> Optional[Item]:
        """Retrieves an inventory item by its location."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_collection_id(self, collection_id: uuid.UUID) -> Optional[Item]:
        """Retrieves an inventory item by its collection ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_brand(self, brand: str) -> Optional[Item]:
        """Retrieves an inventory item by its brand."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_model(self, model: str) -> Optional[Item]:
        """Retrieves an inventory item by its model."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_version(self, version: str) -> Optional[Item]:
        """Retrieves an inventory item by its version."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_collection_name(self, collection_name: str) -> Optional[Item]:
        """Retrieves an inventory item by its collection name."""
        raise NotImplementedError

    # Advanced operations
    @abc.abstractmethod
    async def filter_items(self, **filters) -> list[Item]:
        """Filters inventory items based on multiple criteria."""
        raise NotImplementedError

    @abc.abstractmethod
    async def count_items(self, is_active: Optional[bool] = None) -> int:
        """Counts the total number of inventory items, optionally filtering by active status."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update_item_status(self, item_id: uuid.UUID, is_active: bool) -> None:
        """Updates the active status of an inventory item."""
        raise NotImplementedError

    # Collection operations
    @abc.abstractmethod
    async def add_collection(self, name: str, description: str) -> None:
        """Adds a new collection to the inventory."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_collections(self) -> list:
        """Lists all collections in the inventory."""
        raise NotImplementedError

    @abc.abstractmethod
    async def list_items_by_collection(self, collection_id: uuid.UUID) -> list[Item]:
        """Lists all items belonging to a specific collection."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_items_by_collection(self, collection_id: uuid.UUID) -> None:
        """Deletes all items belonging to a specific collection."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update_collection(
        self, collection_id: uuid.UUID, name: str, description: str
    ) -> None:
        """Updates the details of a collection."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_collection(
        self, collection_id: uuid.UUID, delete_items: bool = True
    ) -> None:
        """Deletes a collection and optionally its associated items."""
        raise NotImplementedError
