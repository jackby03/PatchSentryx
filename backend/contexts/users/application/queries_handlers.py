import uuid
from typing import List, Optional

from pydantic import BaseModel

from contexts.users.application.queries import (GetUserByIdQuery,
                                                ListUsersQuery, UserDTO)
from contexts.users.domain.repositories import UserRepository


class GetUserByIdQueryHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, query: GetUserByIdQuery) -> Optional[UserDTO]:
        print(f"Handling GetUserByIdQuery for user_id: {query.user_id}")
        user = await self.user_repository.get_by_id(query.user_id)
        if not user:
            print(f"User with id {query.user_id} not found.")
            return None
        return UserDTO.model_validate(user)
        # return UserDTO.from_orm(user)


class ListUsersQueryHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, query: ListUsersQuery) -> List[UserDTO]:
        print(
            f"Handling ListUsersQuery with limit: {query.limit}, offset: {query.offset}"
        )
        users = await self.user_repository.list_all()
        filtered_users = users
        if query.is_active is not None:
            filtered_users = [
                user for user in users if user.is_active == query.is_active
            ]

        paginated_users = filtered_users[query.offset : query.offset + query.limit]

        return [UserDTO.model_validate(user) for user in paginated_users]
