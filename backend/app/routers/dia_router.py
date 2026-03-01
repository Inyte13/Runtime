from datetime import date, datetime

from fastapi import APIRouter, Body, Query

from app.core.database import PathDate, QueryDate, SessionDep
from app.schemas.dia_schema import DiaRead, DiaReadDetail, DiaUpdate
from app.services.dia_services import (
  actualizar_dia,
  buscar_dia,
  buscar_dia_detail,
  eliminar_dia,
  mostrar_dias,
  recalcular_hora_final,
)

dia_router = APIRouter(tags=['Dia'])


# GET: Dia básico/detail
@dia_router.get('/dias/{fecha}', response_model=DiaReadDetail | DiaRead)
def get_dia(
  session: SessionDep,
  fecha: PathDate,
  detail: bool = False,
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
  final: date = Query(
    default_factory=lambda: datetime.now().date(),
    description='Por defecto es hoy',
  ),
):
  return mostrar_dias(session, inicio, final)


# POST? NO, se supone que 'todos' los dias ya están creados solo falta actualizarlos


# PATCH: Si 'actualiza' el titulo o el estado y si el dia no existe lo crear automaticamente
@dia_router.patch('/dias/{fecha}', response_model=DiaRead)
def patch_dia(
  session: SessionDep,
  dia: DiaUpdate,
  fecha: PathDate,
):
  return actualizar_dia(session, fecha, dia)


# PATCH: Para actualizar las horas cuando se haga drag and drop
@dia_router.patch('/dias/{fecha}/reordenar', status_code=200)
def sort_bloques(session: SessionDep, fecha: date, ids: list[int] = Body(...)):
  recalcular_hora_final(session, fecha, ids)
  return


# DELETE: Elimina el dia y los bloques que esten dentro
@dia_router.delete('/dias/{fecha}', status_code=204)
def delete_dia(session: SessionDep, fecha: PathDate):
  eliminar_dia(session, fecha)
  return
