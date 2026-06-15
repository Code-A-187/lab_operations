from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.location import LocationCreate, LocationResponse, LocationUpdate
from database import get_async_db
from services.location_service import location_service


router = APIRouter(prefix="/location", tags=["Location"])

@ router.post("/create", response_model = LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(location_in: LocationCreate, db: AsyncSession = Depends(get_async_db)):
    return await location_service.create(db=db, obj_in=location_in)

@ router.get("/list", response_model=List[LocationResponse])
async def read_locations(
    skip: int = 0, 
    limit: int = 100,
    include_inactive: bool = False,
    db: AsyncSession = Depends(get_async_db)
    ):

    return await location_service.get_multi(db=db, skip=skip, limit=limit, include_inactive=include_inactive)

@ router.get("/{location_id}", response_model=LocationResponse)
async def read_location(location_id: int, db: AsyncSession = Depends(get_async_db)):
    return await location_service.get_by_id(db=db, location_id=location_id)

@ router.patch("/{location_id}", response_model=LocationResponse)
async def update_location(location_id: int, location_in: LocationUpdate, db: AsyncSession = Depends(get_async_db)):
    return await location_service.update(db=db, location_id=location_id, obj_in=location_in)
    
@ router.delete("/{location_id}", response_model=LocationResponse)
async def delete_location(location_id: int, db: AsyncSession = Depends(get_async_db)):
    return await location_service.soft_delete(db=db, location_id=location_id)