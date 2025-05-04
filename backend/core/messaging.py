import asyncio
from typing import AsyncGenerator, Optional, TypeAlias

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_fixed)

from app.config import settings
from core.errores import MessagingError

Channel: TypeAlias = AbstractRobustChannel

_connection: Optional[AbstractRobustConnection] = None


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    """Gets or creates the global RabbitMQ connection."""
    global _connection
    if _connection is None or _connection.is_closed:
        print("Attempting to connect to RabbitMQ...")
        _connection = await connect_to_rabbitmq()
        print("RabbitMQ connection established.")
    return _connection


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(
        (asyncio.TimeoutError, aio_pika.exceptions.AMQPConnectionError)
    ),
)
async def connect_to_rabbitmq() -> AbstractRobustConnection:
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL, timeout=10)
        connection.add_close_callback(on_connection_close)
        connection.add_reconnect_callback(on_connection_reconnect)
        return connection
    except (
        ConnectionError,
        asyncio.TimeoutError,
        aio_pika.exceptions.AMQPConnectionError,
    ) as e:
        print(f"Failed to connect to RabbitMQ: {e}. Retrying...")
        raise


def on_connection_close(
    connection: AbstractRobustConnection, exc: Optional[BaseException]
):
    print(f"RabbitMQ connection closed. Exception: {exc}")
    global _connection
    _connection = None


def on_connection_reconnect(connection: AbstractRobustConnection):
    print("RabbitMQ connection reconnected.")


async def close_rabbitmq_connection():
    global _connection
    if _connection and not _connection.is_closed:
        await _connection.close()
        _connection = None
        print("RabbitMQ connection closed.")


async def get_rabbitmq_channel() -> AsyncGenerator[Channel, None]:
    """
    Dependency that provides a RabbitMQ channel for a request.
    """
    connection = await get_rabbitmq_connection()
    channel = None
    try:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        print("RabbitMQ channel acquired.")
        yield channel
    except Exception as e:
        print(f"Error obtaining/using RabbitMQ channel: {e}")
        raise MessagingError(f"Failed to get or use RabbitMQ channel: {e}")
    finally:
        if channel and not channel.is_closed:
            await channel.close()
            print("RabbitMQ channel closed.")


# --- Utility functions for Publishing ---


async def declare_exchange(
    channel: Channel,
    exchange_name: str,
    exchange_type: str = "direct",
    durable: bool = True,
):
    """Declares an exchange."""
    print(
        f"Declaring exchange: {exchange_name}, type: {exchange_type}, durable: {durable}"
    )
    await channel.declare_exchange(
        name=exchange_name, type=aio_pika.ExchangeType(exchange_type), durable=durable
    )


async def declare_queue(
    channel: Channel,
    queue_name: str,
    durable: bool = True,
    arguments: Optional[dict] = None,
):
    """Declares a queue."""
    print(f"Declaring queue: {queue_name}, durable: {durable}")
    await channel.declare_queue(name=queue_name, durable=durable, arguments=arguments)


async def bind_queue(
    channel: Channel,
    queue_name: str,
    exchange_name: str,
    routing_key: str,
):
    """Binds a queue to an exchange."""
    print(
        f"Binding queue: {queue_name} to exchange: {exchange_name} with routing key: {routing_key}"
    )
    queue = await channel.get_queue(queue_name)
    await queue.bind(exchange=exchange_name, routing_key=routing_key)


async def publish_message(
    channel: Channel,
    exchange_name: str,
    routing_key: str,
    body: bytes,
    content_type: str = "application/json",
    delivery_mode: aio_pika.DeliveryMode = aio_pika.DeliveryMode.PERSISTENT,
):
    """Publishes a message to an exchange."""
    print(
        f"Publishing message to exchange: {exchange_name}, routing key: {routing_key}"
    )
    message = aio_pika.Message(
        body=body,
        content_type=content_type,
        delivery_mode=delivery_mode,
    )
    exchange = await channel.get_exchange(exchange_name)
    await exchange.publish(message, routing_key=routing_key)
    print("Message published successfully.")


async def setup_messaing_infrastructure(channel: Channel):
    """Set up necessary exchanges and queues."""
    # Example for User Commands
    user_command_exchange = "user_commands_exchange"
    create_user_queue = "create_user_queue"
    create_user_routing_key = "create_user_routing_key"

    await declare_exchange(
        channel, user_command_exchange, exchange_type="direct", durable=True
    )
    await declare_queue(channel, create_user_queue, durable=True)
    await bind_queue(
        channel, user_command_exchange, create_user_queue, create_user_routing_key
    )
    # Add declarations for other exchanges/queues
    print("Message infrastructure setup complete.")
