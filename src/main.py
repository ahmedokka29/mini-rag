from routes import base, data
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager


# Deprecated: Using lifespan instead of startup and shutdown events for better resource management
# @app.on_event("startup")
# async def startup_db_client():
#     settings = get_settings()
#     app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
#     app.mongodb = app.mongodb_client[settings.MONGODB_DATABASE]

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.mongodb_client.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    settings = get_settings()
    app.state.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.mongodb = app.state.mongodb_client[settings.MONGODB_DATABASE]

    yield

    # === SHUTDOWN ===
    app.state.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
