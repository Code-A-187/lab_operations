import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

# Corrected Imports
from database import engine, Base
from api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Try to connect up to 5 times
    for attempt in range(5):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("Database connected!")
            break
        except Exception as e:
            print(f"Waiting for database... (Attempt {attempt + 1})")
            await asyncio.sleep(2) # Wait 2 seconds before trying again
    yield

app = FastAPI(
    title="Lab Managment System",
    description="API for managing lab equipment and maintenance",
    version="0.1.0",
    lifespan=lifespan
    )


app.include_router(auth_router)

@app.get("/")
def health_check():
    """Simple route to verify the server is alive."""
    return {
        "status": "online",
        "message": "Lab Management API is running"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)