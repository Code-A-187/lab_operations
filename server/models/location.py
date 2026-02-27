from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from .equipment import Equipment

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    building: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    room: Mapped[str] = mapped_column(String(50), nullable=False)
    area_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now)

    equipment: Mapped[List["Equipment"]] = relationship(back_populates="location")