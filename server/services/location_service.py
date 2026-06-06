from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Location
from schemas.location import LocationCreate, LocationUpdate


class LocationService:
    async def create(self, db: AsyncSession, obj_in: LocationCreate) -> Location:
        query = select(Location).where(
            Location.building ==  obj_in.building,
            Location.room == obj_in.room
        )

        result = await db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A location in '{obj_in.building}', room '{obj_in.room}' is already registered."
            )
        
        db_obj = Location(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, location_id: int) -> Location:
        location = await db.get(Location, location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location not found"
            )
        return location
    
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100, include_inactive: bool = False):
        query = select(Location). order_by(Location.building, Location.room)

        if not include_inactive:
            query = query.where(Location.is_active == True)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, location_id: int, obj_in: LocationUpdate) -> Location:
        db_obj = await self.get_by_id(db, location_id)

        # Updates location details dynamically using patch schema values.
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db:AsyncSession, location_id: int) -> Location:
        db_obj = await self.get_by_id(db, location_id)

        db_obj.is_active = False

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
location_service = LocationService()
        
