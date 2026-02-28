from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from models.equipment import EquipmentStatus
from schemas.location import LocationResponse
from schemas.vendor import VendorResponse


class EquipmentBase(BaseModel):
    model: str
    serial_number: str
    name: Optional[str]=None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    status: EquipmentStatus = EquipmentStatus.AVAILABLE
    notes: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    vendor_id: Optional[int] = None
    location_id: Optional[int] = None

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    vendor_id: Optional[int] = None
    location_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    status: Optional[EquipmentStatus] = None
    notes: Optional[str] = None

class EquipmentResponse(EquipmentBase):
    id: int
    creator_id: int # who registered the gear
    vendor_id: Optional[int]
    location_id: Optional[int]
    
    model_config = ConfigDict(from_attributes=True)