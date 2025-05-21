import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from core.database import Base


class ItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    hostname = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    collection_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("collections.id", ondelete="CASCADE"),
        nullable=False,
    )  # Added ondelete="CASCADE" for better referential integrity
    is_active = Column(Boolean, default=True)

    collection = relationship(
        "CollectionModel",
        back_populates="items",
        lazy="joined",  # Use "joined" loading for better performance
    )

    def __repr__(self):
        return f"<InventoryItemModel(id={self.id}, name='{self.name}', hostname='{self.hostname}')>"


class CollectionModel(Base):
    __tablename__ = "collections"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)

    items = relationship(
        "ItemModel",
        back_populates="collection",
        cascade="all, delete-orphan",  # Automatically handle related items
        lazy="selectin",  # Use "selectin" loading for better performance
    )

    def __repr__(self):
        return f"<CollectionModel(id={self.id}, name='{self.name}')>"
