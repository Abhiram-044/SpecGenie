import redis.asyncio as redis
from app.core.config import settings

redis_client: redis.Redis | None = None

async def connect_to_redis():
    global redis_client
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_URL,
            port=settings.REDIS_PORT,
            decode_responses=True,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
        )

        await redis_client.ping()
        print("Redis connected successfully")
    except Exception as e:
        print(f"Redis connection failed: {e}")

async def close_redis_connection():
    global redis_client
    if redis_client:
        await redis_client.close()
        print("Redis connection closed")

def get_redis():
    return redis_client