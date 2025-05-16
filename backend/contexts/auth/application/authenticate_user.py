from pydantic import BaseModel, EmailStr

from contexts.auth.domain.entities import Token
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import UserRepository
from core.errors import AuthorizationError, EntityNotFoundError
from core.security import create_access_token, verify_password


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: str


class AuthenticateUserUseCase:
    """Use case for authenticating a user based on credentials."""

    def __init__(self, user_repository: UserRepository):
        # This use case depends on the UserRepository from the Users context
        self.user_repository = user_repository

    async def execute(self, request: AuthenticateUserRequest) -> Token:
        """
        Authenticates the user and returns an access token upon success.

        Raises:
            EntityNotFoundError: If the user with the given email doesn't exist.
            AuthorizationError: If the password verification fails or user is inactive.
        """
        print(f"Authenticating user: {request.username}")

        user = await self.user_repository.get_by_email(request.username)
        if not user:
            print(f"Authentication failed: User '{request.username}' not found.")
            raise AuthorizationError("Incorrect username or password.")

        if not user.check_password(request.password):
            print(
                f"Authentication failed: Incorrect password for user '{request.username}'."
            )
            raise AuthorizationError("Incorrect username or password.")

        if not user.is_active:
            print(f"Authentication failed: User '{request.username}' is inactive.")
            raise AuthorizationError("User account is inactive.")

        access_token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=access_token_data)

        print(f"User '{request.username}' authenticated successfully.")
        return Token(access_token=access_token, token_type="bearer")
