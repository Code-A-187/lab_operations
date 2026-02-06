
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from schemas.user import UserCreate, UserOut
from core.exceptions import DatabaseError, UserAlreadyExistsError
from services.auth_service import register_new_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # it gets the data from register form use function to check for duplicates, return the registered user
    try:
        return await  register_new_user(db, user_data)
    
    except UserAlreadyExistsError as e:
         # translate domain error to 400 bad request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    
    except DatabaseError as e:
        # translate domain error to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 
            
    

