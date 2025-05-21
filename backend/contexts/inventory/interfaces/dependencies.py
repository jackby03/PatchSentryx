from typing import Annotated

from fastapi import Depends

from contexts.inventory.application.command_handlers import (
    CreateCollectionCommandHandler,
    CreateItemCommandHandler,
    DeleteCollectionCommandHandler,
    DeleteItemCommandHandler,
    MoveItemsCommandHandler,
    UpdateCollectionCommandHandler,
    UpdateItemCommandHandler,
    UpdateItemStatusCommandHandler,
)
from contexts.inventory.application.query_handlers import (
    CountItemsQueryHandler,
    GetItemByIdQueryHandler,
    GetItemsByCollectionQueryHandler,
    ListActiveCollectionsQueryHandler,
    ListActiveItemsQueryHandler,
    ListCollectionsQueryHandler,
    ListItemsQueryHandler,
    SearchItemsQueryHandler,
)
from contexts.inventory.domain.repositories import InventoryRepository
from contexts.inventory.infrastructure.repositories import SQLAlchemyInventoryRepository
from core.dependencies import DbSession  # Use shared session provider


# --- Repository Dependency ---
def get_inventory_repository(session: DbSession) -> InventoryRepository:
    """Provides a concrete InventoryRepository."""
    return SQLAlchemyInventoryRepository(session)


InventoryRepo = Annotated[InventoryRepository, Depends(get_inventory_repository)]


# --- Command Handler Dependencies ---
def get_create_item_handler(repo: InventoryRepo) -> CreateItemCommandHandler:
    return CreateItemCommandHandler(repo)


CreateItemHandler = Annotated[
    CreateItemCommandHandler, Depends(get_create_item_handler)
]


def get_update_item_handler(repo: InventoryRepo) -> UpdateItemCommandHandler:
    return UpdateItemCommandHandler(repo)


UpdateItemHandler = Annotated[
    UpdateItemCommandHandler, Depends(get_update_item_handler)
]


def get_delete_item_handler(repo: InventoryRepo) -> DeleteItemCommandHandler:
    return DeleteItemCommandHandler(repo)


DeleteItemHandler = Annotated[
    DeleteItemCommandHandler, Depends(get_delete_item_handler)
]


def get_update_item_status_handler(
    repo: InventoryRepo,
) -> UpdateItemStatusCommandHandler:
    return UpdateItemStatusCommandHandler(repo)


UpdateItemStatusHandler = Annotated[
    UpdateItemStatusCommandHandler, Depends(get_update_item_status_handler)
]


def get_move_items_handler(repo: InventoryRepo) -> MoveItemsCommandHandler:
    return MoveItemsCommandHandler(repo)


MoveItemsHandler = Annotated[MoveItemsCommandHandler, Depends(get_move_items_handler)]


def get_create_collection_handler(
    repo: InventoryRepo,
) -> CreateCollectionCommandHandler:
    return CreateCollectionCommandHandler(repo)


CreateCollectionHandler = Annotated[
    CreateCollectionCommandHandler, Depends(get_create_collection_handler)
]


def get_update_collection_handler(
    repo: InventoryRepo,
) -> UpdateCollectionCommandHandler:
    return UpdateCollectionCommandHandler(repo)


UpdateCollectionHandler = Annotated[
    UpdateCollectionCommandHandler, Depends(get_update_collection_handler)
]


def get_delete_collection_handler(
    repo: InventoryRepo,
) -> DeleteCollectionCommandHandler:
    return DeleteCollectionCommandHandler(repo)


DeleteCollectionHandler = Annotated[
    DeleteCollectionCommandHandler, Depends(get_delete_collection_handler)
]


# --- Query Handler Dependencies ---
def get_item_by_id_query_handler(repo: InventoryRepo) -> GetItemByIdQueryHandler:
    return GetItemByIdQueryHandler(repo)


GetItemByIdHandler = Annotated[
    GetItemByIdQueryHandler, Depends(get_item_by_id_query_handler)
]


def get_list_items_query_handler(repo: InventoryRepo) -> ListItemsQueryHandler:
    return ListItemsQueryHandler(repo)


ListItemsHandler = Annotated[
    ListItemsQueryHandler, Depends(get_list_items_query_handler)
]


def get_search_items_query_handler(repo: InventoryRepo) -> SearchItemsQueryHandler:
    return SearchItemsQueryHandler(repo)


SearchItemsHandler = Annotated[
    SearchItemsQueryHandler, Depends(get_search_items_query_handler)
]


def get_count_items_query_handler(repo: InventoryRepo) -> CountItemsQueryHandler:
    return CountItemsQueryHandler(repo)


CountItemsHandler = Annotated[
    CountItemsQueryHandler, Depends(get_count_items_query_handler)
]


def get_list_active_items_query_handler(
    repo: InventoryRepo,
) -> ListActiveItemsQueryHandler:
    return ListActiveItemsQueryHandler(repo)


ListActiveItemsHandler = Annotated[
    ListActiveItemsQueryHandler, Depends(get_list_active_items_query_handler)
]


def get_items_by_collection_query_handler(
    repo: InventoryRepo,
) -> GetItemsByCollectionQueryHandler:
    return GetItemsByCollectionQueryHandler(repo)


GetItemsByCollectionHandler = Annotated[
    GetItemsByCollectionQueryHandler, Depends(get_items_by_collection_query_handler)
]


def get_list_collections_query_handler(
    repo: InventoryRepo,
) -> ListCollectionsQueryHandler:
    return ListCollectionsQueryHandler(repo)


ListCollectionsHandler = Annotated[
    ListCollectionsQueryHandler, Depends(get_list_collections_query_handler)
]


def get_list_active_collections_query_handler(
    repo: InventoryRepo,
) -> ListActiveCollectionsQueryHandler:
    return ListActiveCollectionsQueryHandler(repo)


ListActiveCollectionsHandler = Annotated[
    ListActiveCollectionsQueryHandler,
    Depends(get_list_active_collections_query_handler),
]
