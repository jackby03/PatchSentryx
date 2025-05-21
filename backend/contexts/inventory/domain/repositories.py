import abc
import uuid
from typing import Optional

from contexts.inventory.entities import InventoryItem


class InventoryRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, item: InventoryItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_item_by_id(self, item_id: uuid.UUID) -> Optional[InventoryItem]:
        raise NotImplementedError