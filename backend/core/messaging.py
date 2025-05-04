import asyncio
from typing import TypeAlias, Optional

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from tenacity import (retry, retry_if_exception_type, stop_after_attempt, wait_fixed)

from backend.app.config import settings

Channel: TypeAlias = AbstractRobustChannel

_connection: Optional[AbstractRobustConnection] = None


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    """Gets or creates the global RabbitMQ connection."""
    global _connection
    if _connection is None or _connection.is_closed:
        print("Attempting to connect to RabbitMQ...")


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(
        (asyncio.TimeoutError, aio_pika.exceptions.AMQPConnectionError)
    )
)
async def connect_to_rabbitmq() -> AbstractRobustConnection:
    try:
        _connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL, timeout=10
        )
    except (asyncio.TimeoutError, aio_pika.exceptions.AMQPConnectionError) as e:
        print(f"Failed to connect to RabbitMQ: {e}. Retrying...")
        raise