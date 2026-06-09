from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.equipment import EquipmentCreate, EquipmentUpdate
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
        
            if not vendor or not vendor.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Selected vendor is invalid or inactive."
                    )
    
        if obj_in.location_id is not None:
            location = await db.get(Location, obj_in.location_id)

            if not location or not location.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Selected location is invalid or inactive."
                )
        
        db_obj = Equipment(
            **obj_in.model_dump(),
            creator_id=creator_id
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, db:AsyncSession, equipment_id: int) -> Equipment:
        query = select(Equipment).options(
            joinedload(Equipment.vendor),
            joinedload(Equipment.location)).where(
                Equipment.id == equipment_id)
        
        result = await db.execute(query)
        equipment = result.scalars().first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipment not found"
                )
        return equipment
    
    async def get_multi(self, db:AsyncSession, skip: int=0, limit: int =100, include_inactive: bool = False):
        query = select(Equipment).options(
            joinedload(Equipment.vendor),
            joinedload(Equipment.location)).order_by(
                Equipment.created_at.desc())
        
        if not include_inactive:
            query =  query.where(Equipment.is_active == True)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db:AsyncSession, equipment_id: int, obj_in: EquipmentUpdate):
        db_obj = await self.get_by_id(db, equipment_id)

        if obj_in.vendor_id is not None:
            vendor = await db.get(Vendor, obj_in.vendor_id)
            if not vendor or not vendor.is_active:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot reassign to an inactive vendor.")
        if obj_in.location_id is not None:
            location =  await db.get(Location, obj_in.location_id)
            if not location or not location.is_active:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot reassign to an inactive location.")
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def soft_delete(self, db: AsyncSession, equipment_id: int) -> Equipment:
        db_obj = await self.get_by_id(db, equipment_id)
        db_obj.is_active = False

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
equipment_service = EquipmentService()