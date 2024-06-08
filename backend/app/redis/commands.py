import json
from typing import Any

from app.redis.client import RedisClient


class Commands:
    create_user = "create_user"

    @staticmethod
    def get_command_message(command: str, data: Any, dump: bool = False) -> dict:
        message = {
            "command": command,
            "data": data,
        }

        if dump:
            message = json.dumps(message)

        return message


async def send_user(user):
    """
    Отправляет запись о новом юзере в брокер.
    """
    user_data = {
        "id": user.id,
        "username": user.username,
        "password": user.password,
    }
    redis = RedisClient()

    message = Commands.get_command_message(
        command=Commands.create_user,
        data=user_data,
        dump=True,
    )
    await redis.send_message(
        redis.Channel.users,
        message,
    )
