from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.models.actividad import Actividad  # noqa: F401
from app.models.bloque import Bloque  # noqa: F401
from app.models.dia import Dia  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield


app = FastAPI(lifespan=lifespan, title="Runtime App")

origins = [
  "http://localhost:5173",  # Tu futuro Frontend React
  "*",  # Para pruebas, permitimos todo
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/")
def read_root():
  return {"msg": "Runtime API funcionando"}
