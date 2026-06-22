import uuid

from app.api.dependencies import IdUsuarioDep
from app.core.database import SessionDep
from app.core.exceptions.generic import ConflictError, NotFoundError
from app.schemas.actividad import (
  ActividadCreate,
  ActividadResponse,
  ActividadResponseDetail,
  ActividadUpdate,
)
from app.services.actividad_service import actividad_service
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

router = APIRouter(tags=['Actividades'], prefix='/actividades')


@router.post('/', status_code=201, response_model=ActividadResponseDetail)
async def post(
  session: SessionDep, id_usuario: IdUsuarioDep, actividad: ActividadCreate
):
  try:
    return await actividad_service.registrar(session, id_usuario, actividad)
  # Usando el unique del schema
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.patch('/{id}', response_model=ActividadResponse)
async def patch(
  session: SessionDep,
  id_usuario: IdUsuarioDep,
  actividad: ActividadUpdate,
  id: uuid.UUID,
):
  try:
    return await actividad_service.actualizar(
      session, id_usuario, actividad, id
    )
  # Usando el unique del schema
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, id_usuario: IdUsuarioDep, id: uuid.UUID):
  try:
    await actividad_service.eliminar(session, id_usuario, id)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ConflictError as e:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
