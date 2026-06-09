from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from core.deps import get_current_user
from database import get_async_db

from models.user import User
from schemas.equipment import EquipmentCreate, EquipmentResponse, EquipmentUpdate
from services.equipment_service import equipment_service

router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.post('/create', response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    equipment_in: EquipmentCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
    ):

    return await equipment_service.create(
        db=db,
        obj_in = equipment_in,
        creator_id=current_user.id
    )

@ router.get('/list', response_model=List[EquipmentResponse])
async def read_equipments(
    skip: int=0,
    limit: int=100,
    include_inactive: bool=False,
    db:AsyncSession = Depends(get_async_db)
    ):

    return await equipment_service.get_multi(db=db, skip=skip, limit=limit, include_inactive=include_inactive)

@ router.get('/{eqipment_id}', response_model=EquipmentResponse)
async def read_equipment(equipment_id: int, db: AsyncSession = Depends(get_async_db)):
    return await equipment_service.get_by_id(db=db, equipment_id=equipment_id)

@ router.patch("/{equipment_id}", response_model=EquipmentResponse)
async def update_equipment(
    equipment_id: int,
    equipment_in: EquipmentUpdate,
    db: AsyncSession = Depends(get_async_db)
    ):
    return await equipment_service.update(db=db, equipment_id=equipment_id, obj_in=equipment_in)

@ router.delete("/{equipment_id}", response_model=EquipmentResponse)
async def delete_equipment(equipment_id: int, db: AsyncSession =  Depends(get_async_db)):
    return await equipment_service.soft_delete(db=db, equipment_id=equipment_id)