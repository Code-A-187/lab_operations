from fastapi import FastAPI
import uvicorn

# Corrected Imports
from database import engine, Base
from api.auth import router as auth_router



app = FastAPI(
    title="Lab Managment System",
    description="API for managing lab equipment and maintenance",
    version="0.1.0"
    )


app.include_router(auth_router)

@app.on_event("startup")
async def init_db():
    # This is the 'magic' part for Async + SQLAlchemy 2.0
    async with engine.begin() as conn:
        # We run the synchronous 'create_all' inside an async connection
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/")
def health_check():
    """Simple route to verify the server is alive."""
    return {
        "status": "online",
        "message": "Lab Management API is running"
    }

