import aioredis


class RedisClient:
    class Channel:
        users = "users"

    connection: aioredis.Redis = None

    def __init__(self, connection=None) -> None:
        self.connection = self.get_connection()

    def get_connection(self):
        if self.connection is None:
            self.connection = aioredis.from_url("redis://redis")
        return self.connection

    async def send_message(self, channel, message):
        await self.connection.publish(channel, message)
