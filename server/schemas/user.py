from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    TECHNICIAN = "technician"

# needed info to create User
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    

# response(what returns to client) when user is creted
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    massage: str = ("Registration successful. Please verify your email.")

    model_config = ConfigDict(from_atributes = True)

class UserLogin(BaseModel):
    pass