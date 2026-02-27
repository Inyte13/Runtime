from datetime import date, datetime
from datetime import date as date_type
from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.core.database import SessionDep
from app.schemas.dia_schema import DiaRead, DiaReadDetail, DiaUpdate
from app.services.dia_services import (
  actualizar_dia,
  buscar_dia,
  buscar_dia_detail,
  eliminar_dia,
  mostrar_dias,
)

dia_router = APIRouter(tags=['Dia'])

PathDate = Annotated[date, Path(..., example='2026-02-25')]
QueryDate = Annotated[date, Query(..., example='2026-02-25')]



# GET: Dia básico/detail
@dia_router.get('/dias/{fecha}', response_model=DiaReadDetail | DiaRead)
def get_dia(
  session: SessionDep,
  fecha: PathDate,
  detail: bool = Query(False),
):
  if detail:
    dia_db = buscar_dia_detail(session, fecha)
    return DiaReadDetail.model_validate(dia_db)
  dia_db = buscar_dia(session, fecha)
  return DiaRead.model_validate(dia_db)


# GET: Dias básicos entre un rango de fechas incluyendo al inicio y al final
@dia_router.get('/dias', response_model=list[DiaRead])
def get_dias_range(
  session: SessionDep,
  inicio: QueryDate,
  # Default, usa el time del servidor
  final: date_type = Query(
    default_factory=lambda: datetime.now().date(),
    description='Por defecto es hoy',
  ),
):
  return mostrar_dias(session, inicio, final)


# POST? NO, se supone que 'todos' los dias ya están creados solo falta actualizarlos


# PATCH: Si 'actualiza' el titulo o el estado y el dia no existe lo crear automaticamente
@dia_router.patch('/dias/{fecha}', response_model=DiaRead)
def patch_dia(
  session: SessionDep,
  dia: DiaUpdate,
  fecha: PathDate,
):
  return actualizar_dia(session, fecha, dia)


# DELETE: Elimina el dia y los bloques mas
@dia_router.delete('/dias/{fecha}', status_code=204)
def delete_dia(session: SessionDep, fecha: PathDate):
  eliminar_dia(session, fecha)
  return
