import enum
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


if TYPE_CHECKING:
    from .user import User
    from .location import Location
    from .maintenance import MaintenanceRecord
    from .measurements import MeasurementData
    from .vendor import Vendor 


class EquipmentStatus(str, enum.Enum):
    AVAILABLE="available"
    DEPLOYED = "deployed"
    MAINTENANCE = "maintenance"
    SCRAPPED = "scrapped"

class Equipment(Base):

    __tablename__ = "equipment"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.id"))
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id"))

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    purchase_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    warranty_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    status: Mapped[EquipmentStatus] = mapped_column(default=EquipmentStatus.AVAILABLE)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now)

    creator: Mapped["User"] = relationship(back_populates="equipment_created")
    vendor: Mapped[Optional["Vendor"]] = relationship(back_populates="equipment")
    location: Mapped[Optional["Location"]] = relationship(back_populates="equipment")

    maintenance_records: Mapped[List["MaintenanceRecord"]] = relationship(back_populates="equipment")
    measurements: Mapped[List["MeasurementData"]] = relationship(back_populates="equipment")

    