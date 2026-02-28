from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from .equipment import Equipment

class Vendor(Base):

    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contact_person: Mapped[Optional: str] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    specialties: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    equipment: Mapped[List["Equipment"]] = relationship(back_populates="vendor")