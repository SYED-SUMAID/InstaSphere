from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel

from app.database import engine
from app.models import User, Post, Comment, Like, Follow
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create tables if they don't exist
    SQLModel.metadata.create_all(engine)

    yield


app = FastAPI(
    title="InstaSphere API",
    description="A three-tier photo-sharing social media application",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to InstaSphere API",
        "application": "InstaSphere",
        "status": "running"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "application": "InstaSphere API",
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        )