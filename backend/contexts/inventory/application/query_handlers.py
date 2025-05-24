from typing import Optional, List

from sqlalchemy.orm import query

from contexts.inventory.application.queries import (
    GetItemByIdQuery,
    ItemDTO,
    ListItemsQuery,
    GetCollectionByIdQuery,
    CollectionDTO,
    ListCollectionsQuery,
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


class GetCollectionByIdQueryHandler:
    """Handles the GetCollectionByIdQuery."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, query: GetCollectionByIdQuery) -> Optional[CollectionDTO]:
        """
        Executes the query to retrieve a collection by ID.
        Returns:
            CollectionDTO or None if the collection is not found.
        """
        print(f"Handling GetCollectionByIdQuery for ID: {query.collection_id}")
        collection = await self.repository.get_collection_by_id(query.collection_id)
        if not collection:
            print(f"Collection with ID {query.collection_id} not found.")
            return None
        return CollectionDTO.model_validate(collection)


class ListCollectionsQueryHandler:
    """Handles the ListCollectionsQuery."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def handle(self, query: ListCollectionsQuery) -> List[CollectionDTO]:
        """
        Executes the query to retrieve a list of collections.
        """
        print(
            f"Handling ListCollectionsQuery with limit={query.limit}, offset={query.offset}"
        )

        # Fetch collections from the repository with pagination
        collections = await self.repository.list_all_collections()
        paginated_collections = collections[query.offset : query.offset + query.limit]
        return [
            CollectionDTO.model_validate(collection)
            for collection in paginated_collections
        ]
