from fastapi import FastAPI
from contextlib import asynccontextmanager

from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from app import api
from app.models import __beanie_models__
from app.configs.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client: AsyncMongoClient = AsyncMongoClient(settings.MONGO_URI)
        await init_beanie(database=client[settings.MONGO_DB_NAME], document_models=__beanie_models__)
        await client.admin.command('ping')  # Check if the connection is successful
        print("Connected to MongoDB successfully.")
    except ConnectionFailure as e:
        SystemExit.exit(f"Failed to connect to MongoDB: {e}")
        
    yield
    await client.close()

app = FastAPI(
    title="Jobify API",
    description=(
        "Backend API for Jobify — an AI-powered platform for analyzing "
        "candidate resumes against job descriptions and generating "
        "structured candidate evaluations."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api.router)


