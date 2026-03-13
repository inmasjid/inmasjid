from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from app.core.db import Base

class Masjid(Base):
    __tablename__ = "masajid"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=True)
    pincode = Column(String(20), nullable=True)
    latitude = Column(String(50), nullable=False)
    longitude = Column(String(50), nullable=False)
    gmap_link = Column(Text, nullable=True)
    location = Column(Geography(geometry_type="POINT", srid=4326))

    # One-to-many: masjid → salah times
    salah_times = relationship("Salah", back_populates="masjid", cascade="all, delete-orphan")

