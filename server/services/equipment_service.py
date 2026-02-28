from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.equipment import EquipmentCreate
from models.equipment import Equipment
from models.vendor import Vendor
from models.location import Location

class EquipmentService:
    async def create(self, db: AsyncSession, obj_in: EquipmentCreate, creator_id: int):
        query = select(Equipment).where(Equipment.serial_number == obj_in.serial_number)
        result = await db.execute(query)

        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Equipment with serial {obj_in.serial_number} already exists."
            )
        if obj_in.vendor_id is not None:
            vendor = await db.get(Vendor, obj_in.vendor_id)
        
            if not vendor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vendor not found"
                    )
        if obj_in.location_id is not None:
            location = await db.get(Location, obj_in.location_id)

            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Location not found"
                )
        
        db_obj = Equipment(
            **obj_in.model_dump(),
            creator_id=creator_id
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
equipment_service = EquipmentService()