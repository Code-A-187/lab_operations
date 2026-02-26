from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class MaintenanceBase(BaseModel):
    maintenance_type: str
    description: str
    scheduled_date: datetime
    cost: float = 0.0
    status: str = "scheduled"

class MaintenanceCreate(MaintenanceBase):
    equipment_id: int
    vendor_id: Optional[int] = None

class MaintenanceResponse(MaintenanceBase):
    id: int
    equipment_id: int
    user_id: int
    vendor_id: Optional[int]
    completed_date: Optional[datetime]
    next_due_date: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)