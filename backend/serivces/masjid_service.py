from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.masjid_repository import MasjidRepository
from app.schemas.masjid import MasjidCreate, MasjidUpdate

class MasjidService:

    @staticmethod
    async def create_masjid(db: AsyncSession, masjid: MasjidCreate):
        return await MasjidRepository.create(db, masjid)

    @staticmethod
    async def get_masjid(db: AsyncSession, masjid_id: int):
        return await MasjidRepository.get(db, masjid_id)

    @staticmethod
    async def list_masajid(db: AsyncSession, skip: int, limit: int):
        return await MasjidRepository.list(db, skip, limit)

    @staticmethod
    async def update_masjid(db: AsyncSession, masjid_id: int, masjid: MasjidUpdate):
        return await MasjidRepository.update(db, masjid_id, masjid)

    @staticmethod
    async def delete_masjid(db: AsyncSession, masjid_id: int):
        return await MasjidRepository.delete(db, masjid_id)

