from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from database import get_db
from schemas.user import UserCreate, UserOut
from auth_utils import hash_password


router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    pass
