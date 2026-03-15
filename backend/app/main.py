from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database
from app.database.redis import connect_to_redis, close_redis_connection
from app.routes import auth, profile

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

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    
    errors = []
    
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(i) for i in err["loc"][1:]),
            "message": err["msg"],
            "type": err["type"],
            "value": err.get("input")
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": errors
        },
    )
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Resume Builder API",
        version="1.0.0",
        description="API for SpecGenie resume builder",
        routes=app.routes,
    )

    schemas = openapi_schema.get("components", {}).get("schemas", {})
    cleaned = {}

    for key, value in schemas.items():
        simple_name = key.split("__")[-1]
        cleaned[simple_name] = value

    openapi_schema["components"]["schemas"] = cleaned
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.include_router(auth.router)
app.include_router(profile.router)
app.openapi = custom_openapi

@app.get("/")
def home():
    return {
        "message": "SpecGenie Working..."
    }