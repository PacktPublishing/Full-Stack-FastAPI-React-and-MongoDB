from decouple import config
from fastapi import FastAPI

import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# there seems to be a bug with FastAPI's middleware
# https://stackoverflow.com/questions/65191061/fastapi-cors-middleware-not-working-with-get-method/65994876#65994876

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

from motor.motor_asyncio import AsyncIOMotorClient

from routers.cars import router as cars_router


DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)


# define origins
origins = [
    "*",
]

# instantiate the app
app = FastAPI(middleware=middleware)

app.include_router(cars_router, prefix="/cars", tags=["cars"])


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    redis = aioredis.from_url(
        "redis://localhost:6379", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
