from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db_session
from backend.core.messaging import (Channel,  # Import Channel type
                                    get_rabbitmq_channel)

dbSession = Annotated[AsyncSession, Depends(get_db_session)]

dbChannel = Annotated[Channel, Depends(get_rabbitmq_channel)]
