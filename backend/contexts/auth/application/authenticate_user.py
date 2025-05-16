from typing import Optional

from pydantic import BaseModel, EmailStr

from contexts.auth.domain.entities import Token
from contexts.users.domain.entities import User
from contexts.users.domain.repositories import \
    UserRepository  # Depends on Users context repository
from core.errors import AuthorizationError, EntityNotFoundError
from core.security import create_access_token, verify_password


class AuthenticateUserRequest(BaseModel):
    """DTO for the authentication request payload."""

    username: EmailStr  # Using email as username
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

        # 1. Find user by email
        user = await self.user_repository.get_by_email(request.username)
        if not user:
            print(f"Authentication failed: User '{request.username}' not found.")
            # Raise EntityNotFound or generic AuthError depending on security policy
            # Raising a generic error prevents username enumeration
            raise AuthorizationError("Incorrect username or password.")
            # raise EntityNotFoundError("User", request.username)

        # 2. Verify password
        if not user.check_password(request.password):
            print(
                f"Authentication failed: Incorrect password for user '{request.username}'."
            )
            raise AuthorizationError("Incorrect username or password.")

        # 3. Check if user is active (Business Rule)
        if not user.is_active:
            print(f"Authentication failed: User '{request.username}' is inactive.")
            raise AuthorizationError("User account is inactive.")

        # 4. Create Access Token
        # Include user ID and/or email (username) in the token payload ('sub' claim)
        access_token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=access_token_data)

        print(f"User '{request.username}' authenticated successfully.")
        return Token(access_token=access_token, token_type="bearer")
