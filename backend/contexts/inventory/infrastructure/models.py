import uuid

from sqlalchemy import Boolean, Column, String, Uuid

from core.database import Base


class ItemModel(Base):
    """
    SQLAlchemy ORM Model for representing the Item entity in the database.
    This model is used to map the Item entity to a database table.
    """

    __tablename__ = "inventory_items"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    hostname = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    user_id = Column(Uuid(as_uuid=True), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<InventoryItemModel(id={self.id}, name='{self.name}', hostname='{self.hostname}')>"
