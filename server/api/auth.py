
from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from schemas.user import UserCreate, UserOut
from services.auth_service import register_new_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # it gets the data from register form use function to check for duplicates, return the registered user
    return await  register_new_user(db, user_data)
