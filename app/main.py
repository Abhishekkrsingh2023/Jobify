from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from app import api
from app.models import __beanie_models__
from app.configs.settings import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks here
    client: AsyncMongoClient = AsyncMongoClient(Settings.MONGO_URI)
    await init_beanie(database=client[Settings.MONGO_DB_NAME], document_models=__beanie_models__)
    
    try:
        await client.admin.command('ping')  # Check if the connection is successful
        print("Connected to MongoDB successfully.")
    except ConnectionFailure as e:
        SystemExit.exit(f"Failed to connect to MongoDB: {e}")
    
    yield
    # Perform cleanup tasks here
    await client.close()

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api.router)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to my FastAPI application!"}


