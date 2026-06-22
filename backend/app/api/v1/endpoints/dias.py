import uuid

from app.api.dependencies import IdUsuarioDep
from app.core.database import PathDate, QueryDate, SessionDep
from app.core.exceptions.generic import (
  ConflictError,
  InvalidDateRangeError,
  NotFoundError,
)
from app.schemas.bloque import BloqueResponse
from app.schemas.dia import (
  DiaResponse,
  DiaResponseDetail,
  DiaResumen,
  DiaUpdate,
)
from app.services.dia_service import dia_service
from fastapi import APIRouter, Body, HTTPException
from starlette import status

router = APIRouter(tags=['Dias'], prefix='/dias')


@router.get('/{fecha}', response_model=DiaResponseDetail)
async def get(session: SessionDep, id_usuario: IdUsuarioDep, fecha: PathDate):
  try:
    return await dia_service.buscar_detail(session, id_usuario, fecha)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.get('/', response_model=list[DiaResumen])
async def get_resumen(
  session: SessionDep,
  id_usuario: IdUsuarioDep,
  inicio: QueryDate,
  final: QueryDate,
):
  try:
    dias = await dia_service.mostrar_resumen(session, id_usuario, inicio, final)
    return [await dia_service.resumen(session, id_usuario, dia) for dia in dias]
  except InvalidDateRangeError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# POST? NO, se supone que 'todos' los dias ya están creados solo falta actualizarlos


# UPSERT: Si no existe lo creamos
@router.patch('/{fecha}', response_model=DiaResponse)
async def patch(
  session: SessionDep, id_usuario: IdUsuarioDep, dia: DiaUpdate, fecha: PathDate
):
  return await dia_service.actualizar(session, id_usuario, dia, fecha)


@router.patch('/{fecha}/reordenar', response_model=list[BloqueResponse])
async def recalculate_hours(
  session: SessionDep,
  id_usuario: IdUsuarioDep,
  fecha: PathDate,
  ids: list[uuid.UUID] = Body(...),
):
  try:
    return await dia_service.recalcular_horas(session, id_usuario, fecha, ids)
  except ConflictError as e:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete('/{fecha}', status_code=204)
async def delete(
  session: SessionDep, id_usuario: IdUsuarioDep, fecha: PathDate
):
  try:
    await dia_service.eliminar(session, id_usuario, fecha)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
