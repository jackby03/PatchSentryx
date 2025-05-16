from pydantic import BaseModel


class TokenDTO(BaseModel):
    """DTO for returning token information to the client."""

    access_token: str
    token_type: str

    class Config:
        from_attributes = True
