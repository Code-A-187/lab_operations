from core.security import hash_password
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def register_new_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)

    user_dict = user_data.model_dump(exclude={"password"})

    db_user = User(**user_dict, password_hash = hashed_password)
    db_user.is_active = False

    # avoids racing conditions when two users try to register email at same time
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower()

        if "users_email_key" in error_msg:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST, 
                detail = "Email already registered",
                )
        
        if "users_username_key" in error_msg:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST, 
                detail = "Username already taken",
                )
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "Database error",
            )





