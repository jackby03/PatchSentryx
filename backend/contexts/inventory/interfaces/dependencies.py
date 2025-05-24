from typing import Annotated

from fastapi import Depends

from contexts.inventory.application.command_handlers import (
    CreateCollectionCommandHandler,
    CreateItemCommandHandler,
    DeleteCollectionCommandHandler,
    DeleteItemCommandHandler,
    UpdateCollectionCommandHandler,
    UpdateItemCommandHandler,
)
from contexts.inventory.application.query_handlers import (
    GetItemByIdQueryHandler,
    GetCollectionByIdQueryHandler,
    ListCollectionsQueryHandler,
    ListItemsQueryHandler,
)
from contexts.inventory.domain.repositories import InventoryRepository
from contexts.inventory.infrastructure.repositories import SQLAlchemyInventoryRepository
from core.dependencies import DbSession


# --- Repository Dependency ---
def get_inventory_repository(session: DbSession) -> InventoryRepository:
    """Provides a concrete InventoryRepository."""
    return SQLAlchemyInventoryRepository(session)


InventoryRepo = Annotated[InventoryRepository, Depends(get_inventory_repository)]


# ==========================
# Command Handler Dependencies
# ==========================


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


# ==========================
# Query Handler Dependencies
# ==========================


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


def get_collection_by_id_query_handler(
    repo: InventoryRepo,
) -> GetCollectionByIdQueryHandler:
    return GetCollectionByIdQueryHandler(repo)


GetCollectionByIdHandler = Annotated[
    GetCollectionByIdQueryHandler, Depends(get_collection_by_id_query_handler)
]


def get_list_collections_query_handler(
    repo: InventoryRepo,
) -> ListCollectionsQueryHandler:
    return ListCollectionsQueryHandler(repo)


ListCollectionsHandler = Annotated[
    ListCollectionsQueryHandler, Depends(get_list_collections_query_handler)
]
