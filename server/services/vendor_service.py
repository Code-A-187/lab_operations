from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models.vendor import Vendor
from schemas.vendor import VendorCreate, VendorUpdate


class VendorService:
    async def create(self, db:AsyncSession, obj_in:VendorCreate) -> Vendor:
        query = select(Vendor).where(Vendor.company_name == obj_in.company_name)
        result = await db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vendor '{obj_in.company_name}' is already registered"
            )
        
        db_obj = Vendor(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, db: AsyncSession, vendor_id: int) -> Vendor:
        vendor = await db.get(Vendor, vendor_id)
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vendor not found"
            )
        return vendor
    
    async def get_multi(self, db:AsyncSession, skip: int = 0, limit: int = 100, include_inactive: bool = False):
        query = select(Vendor).order_by(Vendor.name)
        
        if not include_inactive:
            query = query.where(Vendor.is_active == True)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, vendor_id: int, obj_in: VendorUpdate) -> Vendor:
        db_obj = await self.get_by_id(db, vendor_id)

        # update data dinamicaly
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        await db_obj
    
    async def soft_delete(self, db: AsyncSession, vendor_id: int) -> Vendor:
        """Flips is_active from True to False without removing the row."""
        db_obj = await self.get_by_id(db, vendor_id)
        
        db_obj.is_active = False
        await db.commit()
        await db.refresh(db_obj)
        return db_obj  

vendor_service = VendorService()
