from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.salah_repository import SalahRepository
from app.schemas.masjid import SalahCreate

class SalahService:

    @staticmethod
    async def create_salah(db: AsyncSession, masjid_id: int, salah: SalahCreate):
        return await SalahRepository.create(db, masjid_id, salah)

    @staticmethod
    async def list_salah_by_masjid(db: AsyncSession, masjid_id: int):
        return await SalahRepository.list_by_masjid(db, masjid_id)

    @staticmethod
    async def delete_salah(db: AsyncSession, masjid_id: int, salah_id: int):
        return await SalahRepository.delete(db, masjid_id, salah_id)

