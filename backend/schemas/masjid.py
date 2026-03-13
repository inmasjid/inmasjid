from pydantic import BaseModel
from typing import Optional, List
from datetime import time

class SalahBase(BaseModel):
    salah: str
    time: time

class SalahCreate(SalahBase):
    pass

class SalahOut(SalahBase):
    id: int
    class Config:
        orm_mode = True

class MasjidBase(BaseModel):
    name: str
    address: Optional[str] = None
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    gmap_link: Optional[str] = None

class MasjidCreate(MasjidBase):
    salah_times: Optional[List[SalahCreate]] = []

class MasjidUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    gmap_link: Optional[str] = None

class MasjidOut(MasjidBase):
    id: int
    salah_times: List[SalahOut] = []
    class Config:
        orm_mode = True

