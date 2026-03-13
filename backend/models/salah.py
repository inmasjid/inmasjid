from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Salah(Base):
    __tablename__ = "salah_times"

    id = Column(Integer, primary_key=True, index=True)
    masjid_id = Column(Integer, ForeignKey("masajid.id", ondelete="CASCADE"))
    salah = Column(String(50), nullable=False)  # e.g., Fajr, Dhuhr, Asr
    time = Column(Time, nullable=False)

    masjid = relationship("Masjid", back_populates="salah_times")

