import uuid
from typing import Any, Optional, Type, TypeVar

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

    # Delegate commands
    async def add_item(self, item: Item) -> None:
        await self.commands.add_item(item)

    async def update(self, item: Item) -> None:
        await self.commands.update_item(item)

    async def delete(self, item_id: uuid.UUID) -> None:
        await self.commands.delete_item(item_id)

    async def update_item_status(self, item_id: uuid.UUID, is_active: bool) -> None:
        await self.commands.update_item_status(item_id, is_active)

    async def move_items_to_collection(
        self, item_ids: list[uuid.UUID], target_collection_id: uuid.UUID
    ) -> None:
        await self.commands.move_items_to_collection(item_ids, target_collection_id)

    async def add_collection(self, name: str, description: str) -> None:
        await self.commands.add_collection(name, description)

    async def update_collection(
        self, collection_id: uuid.UUID, name: str, description: str
    ) -> None:
        await self.commands.update_collection(collection_id, name, description)

    async def delete_collection(
        self, collection_id: uuid.UUID, delete_items: bool = True
    ) -> None:
        await self.commands.delete_collection(collection_id, delete_items)

    # Delegate queries
    async def get_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        return await self.queries.get_item_by_id(item_id)

    async def list_all(self) -> list[Item]:
        return await self.queries.list_all_items()

    async def get_by_collection_id(self, collection_id: uuid.UUID) -> list[Item]:
        return await self.queries.get_items_by_collection_id(collection_id)

    async def search_items(self, query: str) -> list[Item]:
        return await self.queries.search_items(query)

    async def count_items(self, is_active: Optional[bool] = None) -> int:
        return await self.queries.count_items(is_active)

    async def list_active_items(self, is_active: bool = True) -> list[Item]:
        return await self.queries.list_active_items(is_active)

    async def list_collections(self) -> list[Collection]:
        return await self.queries.list_collections()

    async def list_active_collections(self, is_active: bool = True) -> list[Collection]:
        return await self.queries.list_active_collections(is_active)
