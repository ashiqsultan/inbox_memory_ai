from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import hello, postmark, auth, kb
from app.database.database import Database
from app.database.redis_connect import Redis
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting FastAPI in {settings.environment.upper()} mode")
    print("Connecting to database...")
    await Database.connect()
    print("Connecting to Redis...")
    await Redis.connect()
    yield
    await Database.disconnect()
    await Redis.disconnect()
    print("Disconnected from database and Redis")


# Initialize FastAPI app
app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


# Include routers
app.include_router(hello.router)
app.include_router(postmark.router)
app.include_router(auth.router)
app.include_router(kb.router)