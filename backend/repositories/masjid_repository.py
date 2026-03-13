from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from app.models.masjid import Masjid
from app.models.salah import Salah
from app.schemas.masjid import MasjidCreate, MasjidUpdate

class MasjidRepository:

    @staticmethod
    async def create(db: AsyncSession, masjid: MasjidCreate):
        location = from_shape(Point(masjid.longitude, masjid.latitude), srid=4326)
        db_obj = Masjid(
            name=masjid.name,
            address=masjid.address,
            pincode=masjid.pincode,
            latitude=str(masjid.latitude),
            longitude=str(masjid.longitude),
            gmap_link=masjid.gmap_link,
            location=location
        )
        db.add(db_obj)
        await db.flush()

        # Create salah times
        for s in masjid.salah_times or []:
            salah = Salah(salah=s.salah, time=s.time, masjid_id=db_obj.id)
            db.add(salah)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def get(db: AsyncSession, masjid_id: int):
        result = await db.execute(select(Masjid).where(Masjid.id == masjid_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Masjid).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, masjid_id: int, masjid: MasjidUpdate):
        db_obj = await MasjidRepository.get(db, masjid_id)
        if not db_obj:
            return None
        for field, value in masjid.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, masjid_id: int):
        db_obj = await MasjidRepository.get(db, masjid_id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

