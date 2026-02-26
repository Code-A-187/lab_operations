from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# needed info to create User
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    

# response(what returns to client) when user is created
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    verified_at: Optional[datetime] = None

    model_config = ConfigDict(from_atributes = True)

class UserCreateResponse(UserOut):
    message: str = "Registration successful. Please verify your email."

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"