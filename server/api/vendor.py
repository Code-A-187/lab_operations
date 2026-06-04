
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from server.database import get_async_db
from server.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate
from server.services import vendor_service


router = APIRouter(prefix="/vendor", tags=["Vendor"])

@ router.post("/create", response_model = VendorResponse, status_code=status.HTTP_200_OK)
async def create_vendor(vendor_in: VendorCreate, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.create(db=db, obj_in=vendor_in)


@ router.get("/list", responce_model = List[VendorResponse])
async def read_vendors(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_async_db)):
    # fetch all vendors. It is for FE to populate drop down menu, so user can choose proper vendor.
    return await vendor_service.get_multi(db=db, skip=skip, limit=limit)

@ router.get("/{vendor_id}", response_model = VendorResponse)
async def read_vendor(vendor_id: int, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.get_by_id(db=db, vendor_id=vendor_id)

@ router.patch("/{vendor_id}", response_model =  VendorResponse)
async def update_vendor(vendor_id: int, vendor_in: VendorUpdate, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.update(db=db, vendor_id=vendor_id, obj_in=vendor_in)

@router.delete("/{vendor_id}", response_model=VendorResponse)
async def delete_vendor(vendor_id: int, db: AsyncSession = Depends(get_async_db)):
    return await vendor_service.soft_delete(db=db, vendor_id=vendor_id)