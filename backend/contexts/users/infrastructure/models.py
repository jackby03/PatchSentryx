import uuid

from sqlalchemy import Boolean, Column, String, Uuid
from sqlalchemy.orm import relationship  # If relations are needed

from core.database import Base


class UserModel(Base):
    """
    SQLAlchemy ORM Model representing the 'users' table.
    This maps to the database schema.
    """

    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Add relationships here if needed, e.g.:
    # posts = relationship("PostModel", back_populates="author")

    def __repr__(self):
        return f"<UserModel(id={self.id}, email='{self.email}', name='{self.name}')>"
