from sqlalchemy import ForeignKey, String, Text, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime

from database import Base


class MeasurementData(Base):
    __tablename__ = "measurement_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    
    import_batch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("import_batches.id"), index=True)

    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    parameter_type: Mapped[str] = mapped_column(String(100)) # e.g., "Temperature", "pH", "Weight"
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20)) # e.g., "°C", "mg", "RH%"
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    equipment: Mapped["Equipment"] = relationship(back_populates="measurements")
    batch: Mapped[Optional["ImportBatch"]] = relationship(back_populates="measurements")
    user: Mapped["User"] = relationship() # Tracks who owns this data point

class ImportBatch(Base):
    __tablename__ = "import_batches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    uploaded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    record_count: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    notes: Mapped[Optional[str]] = mapped_column(Text)

    measurements: Mapped[list["MeasurementData"]] = relationship(back_populates="batch")
    uploader: Mapped["User"] = relationship()