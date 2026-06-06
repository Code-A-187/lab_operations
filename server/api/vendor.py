
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from database import get_async_db
from schemas.vendor import VendorCreate, VendorResponse, VendorUpdate
from services import vendor_service


router = APIRouter(prefix="/vendor", tags=["Vendor"])

@ router.post("/create", response_model = VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(vendor_in: VendorCreate, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.create(db=db, obj_in=vendor_in)


@ router.get("/list", response_model = List[VendorResponse])
async def read_vendors(
    skip: int = 0, 
    limit: int = 100,
    include_inactive: bool = False,
    db: AsyncSession = Depends(get_async_db)
    ):
    # fetch all vendors. It is for FE to populate drop down menu, so user can choose proper vendor, only activ vendors are shown.
    return await vendor_service.get_multi(db=db, skip=skip, limit=limit, include_inactive=include_inactive)

@ router.get("/{vendor_id}", response_model = VendorResponse)
async def read_vendor(vendor_id: int, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.get_by_id(db=db, vendor_id=vendor_id)

@ router.patch("/{vendor_id}", response_model =  VendorResponse)
async def update_vendor(vendor_id: int, vendor_in: VendorUpdate, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.update(db=db, vendor_id=vendor_id, obj_in=vendor_in)

@router.delete("/{vendor_id}", response_model=VendorResponse)
async def delete_vendor(vendor_id: int, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.soft_delete(db=db, vendor_id=vendor_id)