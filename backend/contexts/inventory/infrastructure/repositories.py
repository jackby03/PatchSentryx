import uuid
from typing import Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from contexts.inventory.domain.entities import Item
from contexts.inventory.domain.repositories import InventoryRepository
from contexts.inventory.infrastructure.commands import InventoryCommands
from contexts.inventory.infrastructure.queries import InventoryQueries

T = TypeVar("T", Item)


class SQLAlchemyInventoryRepository(InventoryRepository):
    def __init__(self, session: AsyncSession):
        self.commands = InventoryCommands(session)
        self.queries = InventoryQueries(session)

    # CRUD operations for Item
    # Query operations
    async def get_item_by_id(self, item_id: uuid.UUID) -> Optional[Item]:
        return await self.queries.get_item_by_id(item_id)

    async def list_all_items(self) -> None:
        return await self.queries.list_all_items()

    # Command operations
    async def add_item(self, item: Item) -> None:
        return await self.commands.add_item(item)

    async def update_item(self, item: Item) -> None:
        return await self.commands.update_item(item)

    async def delete_item(self, item_id: uuid.UUID) -> None:
        return await self.commands.delete_item(item_id)

    # Query operations

    async def search_items(self, query: str) -> None:
        return await self.queries.search_items(query)

    async def count_items(self, is_active: Optional[bool] = None) -> None:
        return await self.queries.count_items(is_active)
