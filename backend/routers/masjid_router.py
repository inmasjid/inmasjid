from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.schemas.masjid import MasjidCreate, MasjidUpdate, MasjidOut
from app.services.masjid_service import MasjidService

router = APIRouter(prefix="/masajid", tags=["Masajid"])

@router.post("/", response_model=MasjidOut)
async def create_masjid(masjid: MasjidCreate, db: AsyncSession = Depends(get_db)):
    return await MasjidService.create_masjid(db, masjid)

@router.get("/{masjid_id}", response_model=MasjidOut)
async def get_masjid(masjid_id: int, db: AsyncSession = Depends(get_db)):
    db_obj = await MasjidService.get_masjid(db, masjid_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Masjid not found")
    return db_obj

@router.get("/", response_model=List[MasjidOut])
async def list_masajid(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await MasjidService.list_masajid(db, skip, limit)

@router.put("/{masjid_id}", response_model=MasjidOut)
async def update_masjid(masjid_id: int, masjid: MasjidUpdate, db: AsyncSession = Depends(get_db)):
    db_obj = await MasjidService.update_masjid(db, masjid_id, masjid)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Masjid not found")
    return db_obj

@router.delete("/{masjid_id}")
async def delete_masjid(masjid_id: int, db: AsyncSession = Depends(get_db)):
    db_obj = await MasjidService.delete_masjid(db, masjid_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Masjid not found")
    return {"message": "Masjid deleted"}

