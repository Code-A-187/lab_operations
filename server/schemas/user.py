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
    password: str = Field(min_length=8)
    username: str = Field(min_length=3)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] =  UserRole.TECHNICIAN

# response(what returns to client) when user is creted
class UserOut(BaseModel):
    id: int
    email: EmailStr
    massage: str = ("Registration successful. Please verify your email.")

    model_config = ConfigDict(from_atributes = True)

class UserLogin(BaseModel):
    pass