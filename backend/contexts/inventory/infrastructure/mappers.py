from typing import Optional

from contexts.inventory.domain.entities import Item
from contexts.inventory.infrastructure.models import ItemModel


def _map_model_to_entity(mode: ItemModel) -> Item:
    return Item(
        id=mode.id,
        name=mode.name,
        hostname=mode.hostname,
        version=mode.version,
        brand=mode.brand,
        model=mode.model,
        serial_number=mode.serial_number,
        location=mode.location,
        user_id=mode.user_id,
        is_active=mode.is_active,
    )


def _map_entity_to_model(
    entity: Item, existing_model: Optional[ItemModel] = None
) -> ItemModel:
    if existing_model:
        existing_model.name = entity.name
        existing_model.hostname = entity.hostname
        existing_model.version = entity.version
        existing_model.brand = entity.brand
        existing_model.model = entity.model
        existing_model.serial_number = entity.serial_number
        existing_model.location = entity.location
        existing_model.user_id = entity.user_id
        existing_model.is_active = entity.is_active
        return existing_model
    else:
        return ItemModel(
            id=entity.id,
            name=entity.name,
            hostname=entity.hostname,
            version=entity.version,
            brand=entity.brand,
            model=entity.model,
            serial_number=entity.serial_number,
            location=entity.location,
            user_id=entity.user_id,
            is_active=entity.is_active,
        )
