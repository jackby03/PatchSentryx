from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db_session
from core.messaging import Channel, get_rabbitmq_channel  # Import Channel type

# Type hint for database session dependency
DbSession = Annotated[AsyncSession, Depends(get_db_session)]

# Type hint for RabbitMQ channel dependency
MqChannel = Annotated[Channel, Depends(get_rabbitmq_channel)]

# Add other common dependencies here if needed
# e.g., get_current_user for authentication
# from contexts.auth.dependencies import get_current_active_user
# from contexts.users.domain.entities import User
# CurrentUser = Annotated[User, Depends(get_current_active_user)]
