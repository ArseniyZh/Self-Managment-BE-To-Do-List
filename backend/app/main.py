import asyncio
import aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import router as api_router
from app.db.base import Base
from app.db.session import async_engine

app = FastAPI()

app.include_router(api_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://95.163.231.52:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# async def consume_redis():
#     redis = await aioredis.create_redis_pool('redis://localhost')
#     channel, = await redis.subscribe('my_channel')
#     redis.publish("my_channel", {"test": "avasv"})
#     async for message in channel.iter():
#         print('Received:', message)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    # asyncio.create_task(consume_redis())
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
