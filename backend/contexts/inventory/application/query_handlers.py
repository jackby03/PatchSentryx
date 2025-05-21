from typing import List, Optional

from contexts.inventory.application.queries import (
    CollectionDTO,
    CountItemsQuery,
    GetItemByIdQuery,
    GetItemsByCollectionQuery,
    ItemDTO,
    ListActiveCollectionsQuery,
    ListActiveItemsQuery,
    ListCollectionsQuery,
    ListItemsQuery,
    SearchItemsQuery,
)
from contexts.inventory.domain.repositories import InventoryRepository


class GetItemByIdQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: GetItemByIdQuery) -> Optional[ItemDTO]:
        print(f"Fetching item by ID: {query.item_id}")
        item = await self.repo.get_by_id(query.item_id)
        if not item:
            raise ValueError(f"Item with ID '{query.item_id}' not found.")
        return ItemDTO.model_validate(item)


class ListItemsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: ListItemsQuery) -> List[ItemDTO]:
        print(
            f"Listing items (active={query.is_active}, limit={query.limit}, offset={query.offset})"
        )
        if query.is_active is not None:
            items = await self.repo.list_active_items(query.is_active)
        else:
            items = await self.repo.list_all()
        # Pagination
        paged = items[query.offset : query.offset + query.limit]
        return [ItemDTO.model_validate(i) for i in paged]


class SearchItemsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: SearchItemsQuery) -> List[ItemDTO]:
        print(f"Searching items with keywords: '{query.query}'")
        if not query.query.strip():
            raise ValueError("Search query cannot be empty.")
        items = await self.repo.search_items(query.query)
        return [ItemDTO.model_validate(i) for i in items]


class CountItemsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: CountItemsQuery) -> int:
        print(f"Counting items (active={query.is_active})")
        return await self.repo.count_items(query.is_active)


class ListActiveItemsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: ListActiveItemsQuery) -> List[ItemDTO]:
        print(f"Listing active items={query.is_active}")
        items = await self.repo.list_active_items(query.is_active)
        return [ItemDTO.model_validate(i) for i in items]


class GetItemsByCollectionQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: GetItemsByCollectionQuery) -> List[ItemDTO]:
        print(f"Fetching items for collection ID: {query.collection_id}")
        # Validate collection exists
        cols = await self.repo.list_collections()
        if not any(c.id == query.collection_id for c in cols):
            raise ValueError(f"Collection '{query.collection_id}' not found.")
        items = await self.repo.get_by_collection_id(query.collection_id)
        return [ItemDTO.model_validate(i) for i in items]


class ListCollectionsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: ListCollectionsQuery) -> List[CollectionDTO]:
        print("Listing all collections")
        cols = await self.repo.list_collections()
        return [CollectionDTO.model_validate(c) for c in cols]


class ListActiveCollectionsQueryHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, query: ListActiveCollectionsQuery) -> List[CollectionDTO]:
        print(f"Listing collections active={query.is_active}")
        cols = await self.repo.list_active_collections(query.is_active)
        return [CollectionDTO.model_validate(c) for c in cols]
