from datetime import date
from fastapi import APIRouter

from backend.app.core.database import SessionDep
from backend.app.schemas.dia_schema import DiaRead
from backend.app.services.dia_services import buscar_dia, mostrar_dias


dia_router = APIRouter(tags=['Dia'])

@dia_router.get('/dias', response_model=list[DiaRead])
def get_dias(session: SessionDep):
  return mostrar_dias(session)


@dia_router.get('/dias/{fecha}', response_model=DiaRead)
def get_dia(session: SessionDep, fecha: date):
  return buscar_dia(session, fecha)


@dia_
