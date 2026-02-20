
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from schemas.user import UserCreate, UserOut, Token, UserLogin
from core.exceptions import DatabaseError, UserAlreadyExistsError
from core.security import create_access_token, verify_email_token, verify_password
from models.user import User
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
    
    
            
@router.get("/verify-email")
async def verify_email(token: str, db:AsyncSession = Depends(get_async_db)):
    # decode and validate token
    user_id = verify_email_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Invalid or expired verification link."
        )
    
    # fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )

    if user.is_active:
        raise HTTPException(status_code=400, detail="Account already verified. Please log in.")
    
    # update the user status
    user.is_active = True
    user.verified_at = datetime.now(timezone.utc)

    await db.commit()

    return {"message": "Email verified successfully! You can now log in."}

@router.post("/login", response_model = Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_async_db)):
    # fetch user aync
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalars().first()

    # if user missing or password is wrong we use generic error message to prevent info leak
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # check if user is verified
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your inbox."
        ) 
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

