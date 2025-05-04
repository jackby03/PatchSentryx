import uuid

from pydantic import Field, BaseModel, EmailStr
from pydantic.v1 import validator

from core.errores import InvalidStateError


class User(BaseModel):
    """
    Domain Entity representing a User.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    hashed_password: str = Field(...)
    is_active: bool = True

    class Config:
        orm_mode = True
        from_attributes = True

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty.")
        return v

    def set_password(self, plain_password: str):
        if not plain_password or len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.hashed_password = self.hash_password(plain_password)

    def check_password(self, plain_password: str) -> bool:
        pass

    def activate(self):
        """Active the user."""
        if self.is_active:
            raise InvalidStateError("User is already active.")
        self.is_active = True

    def deactivate(self):
        """Deactivate the user."""
        if not self.is_active:
            raise InvalidStateError("User is already inactive.")
        self.is_active = False