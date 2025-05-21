import uuid

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from contexts.inventory.domain.entities import Item
from contexts.inventory.infrastructure.mappers import _map_entity_to_model
from contexts.inventory.infrastructure.models import CollectionModel, ItemModel


class InventoryCommands:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_item(self, item: Item) -> None:
        model = _map_entity_to_model(item)
        self.session.add(model)
        await self.session.flush()

    async def update_item(self, item: Item) -> None:
        model = _map_entity_to_model(item)
        await self.session.merge(model)
        await self.session.commit()

    async def delete_item(self, item_id: uuid.UUID) -> None:
        await self.session.execute(delete(ItemModel).where(ItemModel.id == item_id))
        await self.session.commit()

    async def update_item_status(self, item_id: uuid.UUID, is_active: bool) -> None:
        await self.session.execute(
            update(ItemModel).where(ItemModel.id == item_id).values(is_active=is_active)
        )
        await self.session.commit()

    async def move_items_to_collection(
        self, item_ids: list[uuid.UUID], target_collection_id: uuid.UUID
    ) -> None:
        await self.session.execute(
            update(ItemModel)
            .where(ItemModel.id.in_(item_ids))
            .values(collection_id=target_collection_id)
        )
        await self.session.commit()

    async def add_collection(self, name: str, description: str) -> None:
        collection = CollectionModel(name=name, description=description)
        self.session.add(collection)
        await self.session.flush()

    async def update_collection(
        self, collection_id: uuid.UUID, name: str, description: str
    ) -> None:
        await self.session.execute(
            update(CollectionModel)
            .where(CollectionModel.id == collection_id)
            .values(name=name, description=description)
        )
        await self.session.commit()

    async def delete_collection(
        self, collection_id: uuid.UUID, delete_items: bool = True
    ) -> None:
        if delete_items:
            await self.session.execute(
                delete(ItemModel).where(ItemModel.collection_id == collection_id)
            )
        await self.session.execute(
            delete(CollectionModel).where(CollectionModel.id == collection_id)
        )
        await self.session.commit()
