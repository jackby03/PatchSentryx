import json

from aio_pika.abc import AbstractRobustChannel

from contexts.users.application.commands import CreateUserCommand
from core.messaging import (  # Assuming setup is managed elsewhere or called here
    publish_message,
    setup_messaging_infrastructure,
)

# Configuration (could be moved to a central config or context-specific config)
USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_ROUTING_KEY = "user.command.create"


class UserCommandPublisher:
    """Publishes user-related commands to RabbitMQ."""

    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    async def publish_create_user_command(self, command: CreateUserCommand):
        """Publishes a CreateUserCommand."""
        # Ensure exchange exists (optional, could be done at startup)
        # await setup_messaging_infrastructure(self.channel) # Or rely on setup elsewhere

        message_body = command.model_dump_json().encode("utf-8")

        print(f"Publishing CreateUserCommand for email {command.email} to RabbitMQ.")
        await publish_message(
            channel=self.channel,
            exchange_name=USER_COMMAND_EXCHANGE,
            routing_key=CREATE_USER_ROUTING_KEY,
            body=message_body,
            content_type="application/json",
        )
        print("CreateUserCommand published successfully.")

    # Add methods for other commands if needed
    # async def publish_update_user_command(self, command: UpdateUserCommand): ...
