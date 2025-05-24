import uuid
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from contexts.inventory.domain.entities import Item
from contexts.inventory.infrastructure.mappers import _map_model_to_entity
from contexts.inventory.infrastructure.models import ItemModel
from core.errors import DatabaseError


class InventoryQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Query operations for Items
    async def get_item_by_id(self, item_id: uuid.UUID) -> object | None:
        print(f"SQLAlchemy: Getting item by ID: {item_id}")
        try:
            stmt = select(ItemModel).where(ItemModel.id == item_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return _map_model_to_entity(model, Item)
            return None
        except Exception as e:
            print(f"SQLAlchemy: Error getting item by ID: {e}")
            raise DatabaseError(f"Failed to get item by ID: {e}")

    async def list_all_items(self) -> list[object]:
        print(f"SQLAlchemy: Listing all items (Warning: No pagination)")
        try:
            stmt = select(ItemModel).order_by(ItemModel.id)
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            return [_map_model_to_entity(model, Item) for model in models]
        except Exception as e:
            print(f"SQLAlchemy: Error listing all items: {e}")
            raise DatabaseError(f"Failed to list all items: {e}")

    # Additional operations

    async def search_items(self, query: str) -> list[Item]:
        keywords = query.split()
        filters = [
            or_(
                ItemModel.name.ilike(f"%{keyword}%"),
                ItemModel.hostname.ilike(f"%{keyword}%"),
                ItemModel.location.ilike(f"%{keyword}%"),
                ItemModel.brand.ilike(f"%{keyword}%"),
                ItemModel.model.ilike(f"%{keyword}%"),
                ItemModel.serial_number.ilike(f"%{keyword}%"),
            )
            for keyword in keywords
        ]
        stmt = select(ItemModel).where(or_(*filters))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [_map_model_to_entity(model, Item) for model in models]

    async def count_items(self, is_active: Optional[bool] = None) -> int:
        stmt = select(func.count(ItemModel.id))
        if is_active is not None:
            stmt = stmt.where(ItemModel.is_active == is_active)
        result = await self.session.execute(stmt)
        return result.scalar_one()
