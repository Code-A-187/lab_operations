
from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserOut
from services.auth_service import register_new_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = register_new_user(db, user_data)
    
    return new_user
