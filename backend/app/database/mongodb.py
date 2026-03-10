from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global client, db

    client = AsyncIOMotorClient(settings.MONGO_URL)
    print(client)
    db = client[settings.DATABASE_NAME]

    print("MongoDB connected")

async def close_mongo_connection():
    global client

    if client:
        client.close()
        print("MongoDB Disconnected")

def get_database():
    return client[settings.DATABASE_NAME]