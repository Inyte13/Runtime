from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.routers.actividad_router import actividad_router
from app.routers.bloque_router import bloque_router
from app.routers.configuracion_router import configuracion_router
from app.routers.dia_router import dia_router


@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield


app = FastAPI(lifespan=lifespan, title="Runtime App")
app.include_router(actividad_router)
app.include_router(bloque_router)
app.include_router(configuracion_router)
app.include_router(dia_router)

origins = [
  "http://localhost:5173", 
  "*",  # Para pruebas, permitimos todo
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
