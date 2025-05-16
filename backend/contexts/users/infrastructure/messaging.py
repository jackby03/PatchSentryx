import json

from aio_pika.abc import AbstractRobustChannel

from contexts.users.application.commands import CreateUserCommand
from contexts.users.interfaces.consumers.user_consumer import \
    USER_COMMAND_EXCHANGE
from core.messaging import publish_message, setup_messaing_infrastructure

USER_COMMAND_EXCHANGE = "user_commands_exchange"
CREATE_USER_ROUTING_KEY = "user.command.create"


class UserCommandPublisher:
    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    async def publish_create_user_command(self, command: CreateUserCommand):
        message_body = command.model_dump_json().encode("utf-8")
        print(f"Publishing CreateUserCommand for email {command.email} to RabbitMQ.")
        await publish_message(
            channel=self.channel,
            exchange=USER_COMMAND_EXCHANGE,
            routing_key=CREATE_USER_ROUTING_KEY,
            message_body=message_body,
            content_type="application/json",
        )
        print("CreateUserCommand published to successfully.")
