import uuid
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from contexts.auth.application.authenticate_user import AuthenticateUserUseCase
from contexts.auth.domain.entities import TokenData
from contexts.users.domain.entities import User  # Depends on Users context entity
from contexts.users.domain.repositories import (
    UserRepository,
)  # Depends on Users context repo
from contexts.users.interfaces.dependencies import (
    get_user_repository,
)  # Reuse user repo provider
from core.errors import AuthorizationError, EntityNotFoundError
from core.security import decode_access_token

# --- OAuth2 Scheme ---
# Define the URL where the client sends username/password to get a token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)  # Matches the login endpoint path

# --- Use Case Dependency ---


def get_authenticate_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthenticateUserUseCase:
    """Dependency provider for AuthenticateUserUseCase."""
    return AuthenticateUserUseCase(user_repository=user_repo)


# Type hint for AuthenticateUser use case dependency
AuthenticateUser = Annotated[
    AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)
]

# --- Current User Dependency ---


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """
    Dependency to get the current authenticated user based on the token.
    Decodes the token, retrieves the user ID, and fetches the user from the repository.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        print("Token decode failed or token invalid.")
        raise credentials_exception

    # Extract user identifier (e.g., user_id stored in 'sub' claim)
    user_id_str = token_data.get("sub")
    if user_id_str is None:
        print("Subject ('sub') claim missing in token.")
        raise credentials_exception

    try:
        user_id = uuid.UUID(user_id_str)  # Ensure 'sub' is a valid UUID
    except ValueError:
        print(f"Invalid user ID format in token's 'sub' claim: {user_id_str}")
        raise credentials_exception

    # Fetch user from repository
    user = await user_repo.get_by_id(user_id)
    if user is None:
        print(f"User with ID {user_id} from token not found in database.")
        raise credentials_exception  # User might have been deleted after token issuance

    # Optional: Add checks for token revocation here if implemented

    print(f"Successfully authenticated user ID: {user.id} from token.")
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency that builds on get_current_user to ensure the user is active.
    """
    if not current_user.is_active:
        print(f"Authentication failed: User {current_user.id} is inactive.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# Type hints for common authentication dependencies
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ActiveUser = Annotated[User, Depends(get_current_active_user)]
