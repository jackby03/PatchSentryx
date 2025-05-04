import uuid

from sqlalchemy import Boolean, Column, String, Uuid

from core.database import Base


class UserModel(Base):
    """
    SQLAlchemy model for the User entity.
    This model is used to interact with the database.
    """

    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<UserModel(id={self.id}, name={self.name}, email={self.email}, is_active={self.is_active})>"
