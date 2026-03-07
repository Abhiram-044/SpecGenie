from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.database.redis import connect_to_redis, close_redis_connection
from app.routes import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await connect_to_redis()
    yield
    await close_mongo_connection()
    await close_redis_connection()

app = FastAPI(
    title="SpecGenie",
    lifespan=lifespan
)

app.include_router(auth.router)

@app.get("/")
def home():
    return {
        "message": "SpecGenie Working..."
    }