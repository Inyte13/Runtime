import uuid

from app.api.dependencies import IdUsuarioDep, UsuarioDep
from app.core.database import SessionDep
from app.core.exceptions.generic import NotFoundError
from app.core.exceptions.time import (
  InvalidTimeGranularityError,
  TimeBoundaryError,
)
from app.schemas.bloque import BloqueCreate, BloqueResponse, BloqueUpdate
from app.services.bloque_service import bloque_service
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

router = APIRouter(tags=['Bloques'], prefix='/bloques')

# TODO: Un get para traer los bloques para las estadisticas


@router.post('/', status_code=201, response_model=BloqueResponse)
async def post(session: SessionDep, usuario: UsuarioDep, bloque: BloqueCreate):
  try:
    return await bloque_service.registrar(session, usuario, bloque)
  except (InvalidTimeGranularityError, TimeBoundaryError) as e:
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.patch('/{id}', response_model=BloqueResponse)
async def patch(
  session: SessionDep,
  id_usuario: IdUsuarioDep,
  bloque: BloqueUpdate,
  id: uuid.UUID,
):
  try:
    return await bloque_service.actualizar(session, id_usuario, bloque, id)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except TimeBoundaryError as e:
    raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, id_usuario: IdUsuarioDep, id: uuid.UUID):
  try:
    await bloque_service.eliminar(session, id_usuario, id)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except TimeBoundaryError as e:
    raise HTTPException(status_code=400, detail=str(e))
