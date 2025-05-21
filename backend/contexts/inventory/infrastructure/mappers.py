from typing import Any, Type, TypeVar

from contexts.inventory.domain.entities import Collection, Item
from contexts.inventory.infrastructure.models import CollectionModel, ItemModel

T = TypeVar("T", Item, Collection)


def _map_model_to_entity(model: Any, entity_class: Type[T]) -> T:
    """Maps SQLAlchemy model to domain entity."""
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
    """Maps domain entity to SQLAlchemy model."""
    if existing_model := entity.__dict__.get("model"):
        # Update existing model instance
        for key, value in entity.__dict__.items():
            if key != "model" and hasattr(existing_model, key):
                setattr(existing_model, key, value)
        return existing_model
    else:
        # Create new model instance
        if isinstance(entity, Item):
            model_class = ItemModel
        elif isinstance(entity, Collection):
            model_class = CollectionModel
        else:
            raise ValueError(f"Unsupported entity type: {type(entity)}")

        # Convert entity attributes to dict, excluding any attributes not in the model
        model_attrs = {
            k: v
            for k, v in entity.__dict__.items()
            if k != "model" and hasattr(model_class, k)
        }
        return model_class(**model_attrs)
