from typing import Any, Type, TypeVar

from contexts.inventory.domain.entities import Collection, Item
from contexts.inventory.infrastructure.models import CollectionModel, ItemModel

T = TypeVar("T", Item, Collection)


def _map_model_to_entity(model: Any, entity_class: Type[T]) -> T:
    """Maps SQLAlchemy model to domain entity"""
    if not model:
        return None

    if entity_class == Item:
        return Item(
            id=model.id,
            name=model.name,
            hostname=model.hostname,
            version=model.version,
            brand=model.brand,
            model=model.model,
            serial_number=model.serial_number,
            location=model.location,
            collection_id=model.collection_id,
            is_active=model.is_active,
        )
    elif entity_class == Collection:
        return Collection(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            items=[_map_model_to_entity(item, Item) for item in model.items],
        )

    raise ValueError(f"Unsupported entity type: {entity_class}")


def _map_entity_to_model(entity: T) -> Any:
    """Maps domain entity to SQLAlchemy model"""
    if existing_model := entity.__dict__.get("model"):
        # Update existing model instance
        existing_model.name = entity.name
        existing_model.hostname = entity.hostname
        existing_model.version = entity.version
        existing_model.brand = entity.brand
        existing_model.model = entity.model
        existing_model.serial_number = entity.serial_number
        existing_model.location = entity.location
        existing_model.collection_id = entity.collection_id
        existing_model.is_active = entity.is_active
        return existing_model
    else:
        # Create new model instance
        if isinstance(entity, Item):
            return ItemModel(
                id=entity.id,
                name=entity.name,
                hostname=entity.hostname,
                version=entity.version,
                brand=entity.brand,
                model=entity.model,
                serial_number=entity.serial_number,
                location=entity.location,
                collection_id=entity.collection_id,
                is_active=entity.is_active,
            )
        elif isinstance(entity, Collection):
            return CollectionModel(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
            )
