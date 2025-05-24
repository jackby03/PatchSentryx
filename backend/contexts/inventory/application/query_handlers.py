from typing import List, Optional

from contexts.inventory.application.queries import (
    GetItemByIdQuery,
    ItemDTO,
    ListItemsQuery,
)
from contexts.inventory.domain.repositories import InventoryRepository


class GetItemByIdQueryHandler:
    """Handles the GetUserByIdQuery."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, query: GetItemByIdQuery) -> Optional[ItemDTO]:
        """
        Executes the query to retrieve an item by ID.
        Returns:
            ItemDTO or None if the item is not found.
        """
        print(f"Handling GetItemByIdQuery for ID: {query.item_id}")
        item = await self.repository.get_item_by_id(query.item_id)
        if not item:
            print(f"Item with ID {query.item_id} not found.")
            return None
        return ItemDTO.model_validate(item)


class ListItemsQueryHandler:
    """Handles the ListItemsQuery."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, query: ListItemsQuery) -> List[ItemDTO]:
        """
        Executes the query to retrieve a list of items.
        """
        print(
            f"Handling ListItemsQuery with limit={query.limit}, offset={query.offset}"
        )
        items = await self.repository.list_all_items()
        filtered_items = items
        if query.is_active is not None:
            filtered_items = [i for i in items if i.is_active == query.is_active]
        paginated_items = filtered_items[query.offset : query.offset + query.limit]
        return [ItemDTO.model_validate(item) for item in paginated_items]

