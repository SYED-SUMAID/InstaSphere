from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
from app.routes.auth import router as auth_router


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="InstaSphere API",
    description="A three-tier photo-sharing social media application",
    version="1.0.0"
)


# ==========================================
# REGISTER ROUTERS
# ==========================================

app.include_router(auth_router)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Welcome to InstaSphere API",
        "application": "InstaSphere",
        "status": "running"
    }


# ==========================================
# DATABASE HEALTH CHECK
# ==========================================

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