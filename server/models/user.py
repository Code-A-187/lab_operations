from datetime import datetime
from sqlalchemy import Boolean, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    TECHNICIAN = "technician"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default=UserRole.TECHNICIAN)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # equipment_created: Mapped[list["Equipment"]] = relationship("Equipment", back_populates="creator")
    # maintenance_records: Mapped[list["MaintenanceLog"]] = relationship("MaintenanceLog", back_populates="technician")