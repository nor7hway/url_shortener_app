import aioredis
from os import environ


REDIS_HOST = environ.get("REDIS_HOST")
REDIS_DB = environ.get("REDIS_DB")

REDIS_URL = f"redis://{REDIS_HOST}:6379/{REDIS_DB}?encoding=utf-8"


async def get_redis(db: int = 0):
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis
