from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "manager"
    MANAGER = "manager"
    TECHNICIAN = "technician"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash= Column(String, nullable=False)
    role = Column(String, default=UserRole.TECHNICIAN)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updatet_at = Column(DateTime(timezone=True), server_onupdate=func.now())

    equipment_created = relationship("Equipment", back_populates="creator")
    maintenance_records = relationship("MaintenanceLog", back_populates="technician")