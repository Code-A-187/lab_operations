from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class MeasurementBase(BaseModel):
    measured_at: datetime
    parameter_type: str
    value: float
    unit: str
    notes: Optional[str] = None

class MeasurementCreate(MeasurementBase):
    equipment_id: int

class MeasurementResponse(MeasurementBase):
    id: int
    equipment_id: int
    user_id: int
    import_batch_id: Optional[int]
    
    model_config = ConfigDict(from_attributes=True)

class ImportBatchResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    record_count: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)