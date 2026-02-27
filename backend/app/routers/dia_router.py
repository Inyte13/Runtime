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

dia_router = APIRouter(tags=["Dia"])

FechaPath = Annotated[date, Path(..., example='2026-02-25')]


# GET: Dia básico/detail
@dia_router.get('/dias/{fecha}', response_model=DiaReadDetail | DiaRead)
def get_dia(
  session: SessionDep,
  fecha: FechaPath,
  detail: bool = Query(False),
):
  if detail:
    dia_db = buscar_dia_detail(session, fecha)
    return DiaReadDetail.model_validate(dia_db)
  dia_db = buscar_dia(session, fecha)
  return DiaRead.model_validate(dia_db)

@dia_router.get("/dias", response_model=list[DiaRead])
def get_dias_range(session: SessionDep, fecha_inicio: date, fecha_final: date):
  return mostrar_dias(session, fecha_inicio, fecha_final)




@dia_router.post("/dias", response_model=DiaRead)
def post_dia(session: SessionDep, dia: DiaCreate):
  return registrar_dia(session, dia)

@dia_router.patch("/dias/{fecha}", response_model=DiaRead)
def patch_dia(session: SessionDep, fecha: date, dia: DiaUpdate):
  return actualizar_dia(session, fecha, dia)


@dia_router.delete("/dias/{fecha}", status_code=204)
def delete_dia(session: SessionDep, fecha: date):
  eliminar_dia(session, fecha)
  return
