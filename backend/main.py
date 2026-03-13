from fastapi import FastAPI
from app.routers import masjid_router

app = FastAPI(title="InMasjid API", version="0.2.0")

app.include_router(masjid_router.router)

