import uuid
from typing import Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from contexts.inventory.domain.entities import Collection, Item
from contexts.inventory.domain.repositories import InventoryRepository
from contexts.inventory.infrastructure.commands import InventoryCommands
from contexts.inventory.infrastructure.queries import InventoryQueries

T = TypeVar("T", Item, Collection)


class SQLAlchemyInventoryRepository(InventoryRepository):
    def __init__(self, session: AsyncSession):
        self.commands = InventoryCommands(session)
        self.queries = InventoryQueries(session)

    # CRUD operations for Item
    # Query operations
    async def get_item_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        await self.queries.get_item_by_id(item_id)

    async def list_all_items(self) -> None:
        await self.queries.list_all_items()

    # Command operations
    async def add_item(self, item: Item) -> None:
        await self.commands.add_item(item)

    async def update_item(self, item: Item) -> None:
        await self.commands.update_item(item)

    async def delete_item(self, item_id: uuid.UUID) -> None:
        await self.commands.delete_item(item_id)

    # CRUD operations for Collection
    # Query operations
    async def get_collection_by_id(
        self, collection_id: uuid.UUID
    ) -> Optional[Collection]:
        await self.queries.get_collection_by_id(collection_id)

    async def list_all_collections(self) -> None:
        await self.list_all_collections()

    # Command operations
    async def add_collection(self, collection: Collection) -> None:
        await self.commands.add_collection(collection)

    async def update_collection(self, collection: Collection) -> None:
        await self.commands.update_collection(collection)

    async def delete_collection(
        self, collection_id: uuid.UUID, delete_items: bool = True
    ) -> None:
        await self.commands.delete_collection(collection_id)

    # Additional operations
    async def get_items_by_collection_id(self, collection_id: uuid.UUID) -> None:
        await self.queries.get_items_by_collection_id(collection_id)

    async def search_items(self, query: str) -> None:
        await self.queries.search_items(query)

    async def count_items(self, is_active: Optional[bool] = None) -> None:
        await self.queries.count_items(is_active)
