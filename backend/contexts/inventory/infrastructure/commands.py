import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from contexts.inventory.domain.entities import Item
from contexts.inventory.domain.entities import Collection
from contexts.inventory.infrastructure.mappers import _map_entity_to_model
from contexts.inventory.infrastructure.models import CollectionModel, ItemModel
from core.errors import DatabaseError


class InventoryCommands:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Command operations for Items
    async def add_item(self, item: Item) -> None:
        print(f"SQLAlchemy: Adding item {item.name} to database.")
        model = _map_entity_to_model(item)
        try:
            self.session.add(model)
            await self.session.flush([model])
            print(f"SQLAlchemy: Flushed item {item.id}.")
        except Exception as e:
            print(f"SQLAlchemy: Error adding item: {e}")
            raise DatabaseError(f"Failed to add item: {e}")

    async def update_item(self, item: Item) -> None:
        print(f"SQLAlchemy: Updating item {item.id}")
        try:
            model = await self.session.get(ItemModel, item.id)
            if not model:
                raise DatabaseError(f"Item with ID {item.id} not found for update.")
            _map_entity_to_model(item, model)
            await self.session.flush([model])
            print(f"SQLAlchemy: Flushed item {item.id}.")
        except Exception as e:
            print(f"SQLAlchemy: Error updating item: {e}")
            raise DatabaseError(f"Failed to update item: {e}")

    async def delete_item(self, item_id: uuid.UUID) -> None:
        print(f"SQLAlchemy: Deleting item {item_id}")
        try:
            stmt = delete(ItemModel).where(ItemModel.id == item_id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                print(f"SQLAlchemy: Item {item_id} not found for deletion.")
            else:
                print(f"SQLAlchemy: Item {item_id} deleted successfully.")

            await self.session.flush()
        except Exception as e:
            print(f"SQLAlchemy: Error deleting item: {e}")
            raise DatabaseError(f"Failed to delete item: {e}")

    # Command operations for Collections
    async def add_collection(self, collection: Collection) -> None:
        print(f"SQLAlchemy: Adding collection {collection} to database.")
        model = _map_entity_to_model(collection)
        try:
            self.session.add(model)
            await self.session.flush([model])
            print(f"SQLAlchemy: Flushed collection {model.id}.")
        except Exception as e:
            print(f"SQLAlchemy: Error adding collection: {e}")
            raise DatabaseError(f"Failed to add collection: {e}")

    async def update_collection(
        self,
        collection: Collection,
    ) -> None:
        print(f"SQLAlchemy: Updating collection {collection.id}")
        try:
            model = await self.session.get(CollectionModel, collection.id)
            if not model:
                raise DatabaseError(
                    f"Collection with ID {collection.id} not found for update."
                )
            _map_entity_to_model(collection, model)
            await self.session.flush([model])
            print(f"SQLAlchemy: Flushed collection {model.id}.")
        except Exception as e:
            print(f"SQLAlchemy: Error updating collection: {e}")
            raise DatabaseError(f"Failed to update collection: {e}")

    async def delete_collection(
        self,
        collection_id: uuid.UUID,
    ) -> None:
        print(f"SQLAlchemy: Deleting collection {collection_id}")
        try:
            stmt = delete(CollectionModel).where(CollectionModel.id == collection_id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                print(f"SQLAlchemy: Collection {collection_id} not found for deletion.")
            else:
                print(f"SQLAlchemy: Collection {collection_id} deleted successfully.")
            await self.session.flush()
        except Exception as e:
            print(f"SQLAlchemy: Error deleting collection: {e}")
            raise DatabaseError(f"Failed to delete collection: {e}")
