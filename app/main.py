from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from beanie import init_beanie
from pymongo import AsyncMongoClient

from app import api
from app.models import __beanie_models__
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    client: AsyncMongoClient = None
    try:
        client = AsyncMongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
        await init_beanie(database=client[settings.MONGO_DB_NAME], document_models=__beanie_models__)
        await client.admin.command('ping')  # Check if the connection is successful
    except Exception as e:
        SystemExit(f"DATABASE CONNECTION ERROR: {e}")
        
    yield
    if client:
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

origins = [settings.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)


