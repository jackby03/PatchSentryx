import uuid
from typing import List

from contexts.inventory.application.commands import (
    CreateCollectionCommand,
    CreateItemCommand,
    DeleteCollectionCommand,
    DeleteItemCommand,
    MoveItemsCommand,
    UpdateCollectionCommand,
    UpdateItemCommand,
    UpdateItemStatusCommand,
)
from contexts.inventory.domain.entities import Item
from contexts.inventory.domain.repositories import InventoryRepository


# --- Item Commands ---
class CreateItemCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: CreateItemCommand) -> Item:
        print(f"CreateItem: checking existence for {cmd.name}")
        existing = await self.repo.get_by_name(cmd.name)
        if existing:
            raise ValueError(f"Item '{cmd.name}' already exists.")
        item = Item(**cmd.dict())
        print(f"CreateItem: creating {item}")
        await self.repo.add_item(item)
        print(f"CreateItem: created with id {item.id}")
        return item


class UpdateItemCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: UpdateItemCommand) -> Item:
        print(f"UpdateItem: loading item {cmd.id}")
        existing = await self.repo.get_by_id(cmd.id)
        if not existing:
            raise ValueError(f"Item id '{cmd.id}' not found.")
        # update fields
        item = Item(**cmd.dict())
        print(f"UpdateItem: updating to {item}")
        await self.repo.update(item)
        return item


class DeleteItemCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: DeleteItemCommand) -> uuid.UUID:
        print(f"DeleteItem: loading item {cmd.id}")
        existing = await self.repo.get_by_id(cmd.id)
        if not existing:
            raise ValueError(f"Item id '{cmd.id}' not found.")
        print(f"DeleteItem: deleting {cmd.id}")
        await self.repo.delete(cmd.id)
        return cmd.id


class UpdateItemStatusCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: UpdateItemStatusCommand) -> None:
        print(f"UpdateStatus: loading item {cmd.id}")
        existing = await self.repo.get_by_id(cmd.id)
        if not existing:
            raise ValueError(f"Item id '{cmd.id}' not found.")
        print(f"UpdateStatus: setting active={cmd.is_active} for {cmd.id}")
        await self.repo.update_item_status(cmd.id, cmd.is_active)


class MoveItemsCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: MoveItemsCommand) -> List[uuid.UUID]:
        print(f"MoveItems: validating item IDs {cmd.item_ids}")
        for item_id in cmd.item_ids:
            if not await self.repo.get_by_id(item_id):
                raise ValueError(f"Item id '{item_id}' not found.")
        print(f"MoveItems: moving to collection {cmd.target_collection_id}")
        await self.repo.move_items_to_collection(cmd.item_ids, cmd.target_collection_id)
        return cmd.item_ids


# --- Collection Commands ---
class CreateCollectionCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: CreateCollectionCommand) -> None:
        print(f"CreateCollection: checking name '{cmd.name}'")
        cols = await self.repo.list_collections()
        if any(c.name == cmd.name for c in cols):
            raise ValueError(f"Collection '{cmd.name}' already exists.")
        print("CreateCollection: creating")
        await self.repo.add_collection(cmd.name, cmd.description)


class UpdateCollectionCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: UpdateCollectionCommand) -> None:
        print(f"UpdateCollection: loading {cmd.id}")
        cols = await self.repo.list_collections()
        if not any(c.id == cmd.id for c in cols):
            raise ValueError(f"Collection id '{cmd.id}' not found.")
        print(f"UpdateCollection: updating name '{cmd.name}'")
        await self.repo.update_collection(cmd.id, cmd.name, cmd.description)


class DeleteCollectionCommandHandler:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def handle(self, cmd: DeleteCollectionCommand) -> None:
        print(f"DeleteCollection: loading {cmd.id}")
        cols = await self.repo.list_collections()
        if not any(c.id == cmd.id for c in cols):
            raise ValueError(f"Collection id '{cmd.id}' not found.")
        print(f"DeleteCollection: deleting, delete_items={cmd.delete_items}")
        await self.repo.delete_collection(cmd.id, delete_items=cmd.delete_items)
