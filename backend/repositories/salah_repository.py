from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.salah import Salah
from app.models.masjid import Masjid
from app.schemas.masjid import SalahCreate

class SalahRepository:

    @staticmethod
    async def create(db: AsyncSession, masjid_id: int, salah: SalahCreate):
        # Ensure masjid exists
        masjid = await db.get(Masjid, masjid_id)
        if not masjid:
            return None

        db_obj = Salah(
            salah=salah.salah,
            time=salah.time,
            masjid_id=masjid_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def list_by_masjid(db: AsyncSession, masjid_id: int):
        result = await db.execute(select(Salah).where(Salah.masjid_id == masjid_id))
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, masjid_id: int, salah_id: int):
        salah = await db.get(Salah, salah_id)
        if not salah or salah.masjid_id != masjid_id:
            return None
        await db.delete(salah)
        await db.commit()
        return salah

