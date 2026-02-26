from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    building: str
    room: str
    area_description: Optional[str] = None
    notes: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    building: Optional[str] = None
    room: Optional[str] = None
    area_description: Optional[str] = None
    notes: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)