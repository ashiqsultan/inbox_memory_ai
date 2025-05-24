from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import hello, users
from app.database.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    await Database.connect()
    yield
    await Database.disconnect()
    print("Disconnected from database")


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# Include routers
app.include_router(hello.router)
app.include_router(users.router)
