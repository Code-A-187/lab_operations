from sqlalchemy import ForeignKey, String, Text, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime

from database import Base
from models.equipment import Equipment
from models.user import User
from models.vendor import Vendor

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    

    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.id"))

    maintenance_type: Mapped[str] = mapped_column(String(100)) # e.g., "Calibration", "Repair"
    description: Mapped[str] = mapped_column(Text)
    
    scheduled_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="scheduled") # e.g., "pending", "done"

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    equipment: Mapped["Equipment"] = relationship(back_populates="maintenance_records")
    technician: Mapped["User"] = relationship(back_populates="maintenance_records")
    service_provider: Mapped[Optional["Vendor"]] = relationship()