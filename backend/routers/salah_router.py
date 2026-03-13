from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.schemas.masjid import SalahCreate, SalahOut
from app.services.salah_service import SalahService

router = APIRouter(prefix="/salah", tags=["Salah"])

@router.post("/{masjid_id}/salah", response_model=SalahOut)
async def add_salah(masjid_id: int, salah: SalahCreate, db: AsyncSession = Depends(get_db)):
    db_obj = await SalahService.create_salah(db, masjid_id, salah)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Masjid not found")
    return db_obj

@router.get("/{masjid_id}/salah", response_model=List[SalahOut])
async def list_salah(masjid_id: int, db: AsyncSession = Depends(get_db)):
    return await SalahService.list_salah_by_masjid(db, masjid_id)

@router.delete("/{masjid_id}/salah/{salah_id}")
async def delete_salah(masjid_id: int, salah_id: int, db: AsyncSession = Depends(get_db)):
    db_obj = await SalahService.delete_salah(db, masjid_id, salah_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Salah not found")
    return {"message": "Salah deleted"}
