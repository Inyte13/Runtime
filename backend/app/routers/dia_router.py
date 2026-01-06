from datetime import date

from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.dia_schema import DiaRead, DiaUpdate
from app.services.dia_services import (
  actualizar_dia,
  buscar_dia,
  generar_dia,
  mostrar_dias,
)

dia_router = APIRouter(tags=["Dia"])


@dia_router.get("/dias", response_model=list[DiaRead])
def get_dias(session: SessionDep):
  return mostrar_dias(session)


@dia_router.get("/dias/{fecha}", response_model=DiaRead)
def get_dia(session: SessionDep, fecha: date):
  return buscar_dia(session, fecha)


@dia_router.post("/dias/generar", response_model=DiaRead)
def generate_dia(fecha: date, session: SessionDep):
  return generar_dia(session, fecha)


@dia_router.patch("/dias/{fecha}", response_model=DiaRead)
def patch_dia(session: SessionDep, fecha: date, dia: DiaUpdate):
  return actualizar_dia(session, fecha, dia)
