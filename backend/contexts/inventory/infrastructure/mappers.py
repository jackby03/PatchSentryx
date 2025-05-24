from typing import Optional, Type, TypeVar

T = TypeVar("T")
M = TypeVar("M")


def _map_model_to_entity(model: M, entity_class: Type[T]) -> T:
    """
    Maps an SQLAlchemy model instance to a domain entity instance.
    The mapping uses shared attribute names between the model and the entity class.

    Args:
        model: The SQLAlchemy model instance to map from.
        entity_class: The target domain entity class.

    Returns:
        An instance of the target domain entity class.
    """
    entity_fields = (
        entity_class.__annotations__
    )  # Get fields defined in the domain entity
    mapped_data = {
        field: getattr(model, field, None)
        for field in entity_fields
        if hasattr(model, field)
    }

    return entity_class(**mapped_data)


def _map_entity_to_model(
    entity: T, model_class: Type[M], existing_model: Optional[M] = None
) -> M:
    """
    Maps a domain entity instance to an SQLAlchemy model instance.
    If an existing model is provided, it is updated with the entity's values.

    Args:
        entity: The domain entity instance to map from.
        model_class: The target SQLAlchemy model class.
        existing_model: An optional existing SQLAlchemy model instance to update.

    Returns:
        An instance of the SQLAlchemy model.
    """
    entity_fields = entity.__annotations__  # Get fields defined in the domain entity
    if existing_model:
        # Update the existing model with the entity's field values
        for field in entity_fields:
            if hasattr(existing_model, field) and hasattr(entity, field):
                setattr(existing_model, field, getattr(entity, field))
        return existing_model

    # Create a new model instance with the entity's field values
    mapped_data = {
        field: getattr(entity, field)
        for field in entity_fields
        if hasattr(model_class, field)
    }
    return model_class(**mapped_data)
