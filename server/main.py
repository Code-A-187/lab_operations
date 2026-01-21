from fastapi import FastAPI

# Corrected Imports
from database import engine, Base

from api.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Lab Managment System",
    description="API for managing lab equipment and maintenance",
    version="0.1.0"
    )


app.include_router(auth_router)

@app.get("/")
def health_check():
    """Simple route to verify the server is alive."""
    return {
        "status": "online",
        "message": "Lab Management API is running"
    }