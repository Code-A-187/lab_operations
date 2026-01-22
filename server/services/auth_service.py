from sqlalchemy import select, or_
from core.security import hash_password
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


async def register_new_user(db: AsyncSession, user_data: UserCreate):
    # we make single query to find any user with email or username that new user is trying to use, so there are no duplicates
    query = select(User).where(
        or_(User.email == user_data.email, User.username == user_data.username) # we can use "|" instead of "_or" but need to watch for the right parentesis
    )

    result = await db.execute(query) # awaits the database to make (execute) the query
    existing_users = result.scalars().all() # return list of all found users if there are any

    errors = []

    if existing_users: # if any user found in the query above
        for u in existing_users: 
            if u.email == user_data.email: # check if email is used from any user
                errors.append("Email is already registered.")
            if u.username == user_data.username:
                errors.append("Username is already taken") # check if username is used from any user
            
            # raise error and returns list with errors for FE to know what to show to the user. That way user will know what to change so only unique email and username are used.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors
            )
    # after unique check is done we put pasword in hash function
    hashed_password = hash_password(user_data.password)

    # creatinf new user instance 
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        is_active=False
    )

    try: # try to save user in DB and return it
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    except Exception as e: # if something went wrong with DB when try to save new user return error 500
        await db.rollback()
        print(f"Database error {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "Technical error occurred while saving the new user",
            )





