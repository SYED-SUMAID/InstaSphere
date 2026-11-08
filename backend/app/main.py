from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


from app.database import engine

app = FastAPI(title="InstaSphere API", 
              description="Backend API for photo sharing and social media platform",
              version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the InstaSphere API!",
            "status":"running"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"application": "InstaSphere",
                "status": "healthy",
                "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail={"status": "Unhealthy" ,
                            "database": "disconnected"
                    
                    }
                
                )

    