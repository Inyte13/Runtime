from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.core.database import SessionDep
from app.crud.actividad_crud import create_actividad
from app.models.actividad import Actividad
from app.schemas.actividad_schema import (
  ActividadCreate,
  ActividadRead,
  ActividadReadDetail,
  ActividadUpdate,
)
from app.services.actividad_service import (
  actualizar_actividad,
  eliminar_actividad,
  mostrar_actividades,
)

actividad_router = APIRouter(tags=['Actividades'])


# GET: Todas las actividades, puede ser None para traer activos e inactivos
@actividad_router.get('/actividades', response_model=list[ActividadReadDetail])
def get_actividades(session: SessionDep, is_active: bool | None = None):
  try:
    return mostrar_actividades(session, is_active)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))


@actividad_router.post(
  '/actividades', status_code=201, response_model=ActividadReadDetail
)
def post_actividad(session: SessionDep, actividad: ActividadCreate):
  try:
    actividad_detail = create_actividad(
      session, Actividad.model_validate(actividad)
    ).model_dump()
    actividad_detail['tiene_bloques'] = False
    return ActividadReadDetail(**actividad_detail)
  # Usando el unique del schema
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )


@actividad_router.patch('/actividades/{id}', response_model=ActividadRead)
def patch_actividad(session: SessionDep, actividad: ActividadUpdate, id: int):
  try:
    return actualizar_actividad(session, id, actividad)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )


@actividad_router.delete('/actividades/{id}', status_code=204)
def delete_actividad(session: SessionDep, id: int):
  try:
    eliminar_actividad(session, id)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
