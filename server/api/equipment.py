from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from core.deps import get_current_user
from database import get_async_db

from models.user import User
from schemas.equipment import EquipmentCreate, EquipmentResponse
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
