import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import jwt

from database import get_async_db
from models.user import User

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "H256")

# tells fastapi where to look for the token /login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession =  Depends(get_async_db)     
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try: 
        # to decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # fetch user from db
    result = await db.execute(select(User).where(User.id == int(user_id)))

    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user

async def get_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    # check if they are active AND have a verification timestamp
    if not current_user.is_active or current_user.verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires a verified email address."
        )
    return current_user
