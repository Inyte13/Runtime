from fastapi import APIRouter

from app.core.database import SessionDep
from app.crud.actividad_crud import read_actividades
from app.schemas.actividad_schema import (
  ActividadCreate,
  ActividadRead,
  ActividadUpdate,
)
from app.services.actividad_service import (
  actualizar_actividad,
  eliminar_actividad_hard,
  eliminar_actividad_soft,
  registrar_actividad,
)

actividad_router = APIRouter(tags=['Actividades'])


# GET: Todas las actividades, puede ser None para traer activos/inactivos
@actividad_router.get('/actividades', response_model=list[ActividadRead])
def get_actividades(session: SessionDep, is_active: bool | None = None):
  return read_actividades(session, is_active)


@actividad_router.post(
  '/actividades', status_code=201, response_model=ActividadRead
)
def post_actividad(session: SessionDep, actividad: ActividadCreate):
  return registrar_actividad(session, actividad)


@actividad_router.patch('/actividades/{id}', response_model=ActividadRead)
def patch_actividad(session: SessionDep, actividad: ActividadUpdate, id: int):
  return actualizar_actividad(session, id, actividad)


# Aunque sea soft delete, igual va delete
@actividad_router.delete('/actividades/{id}', status_code=204)
def delete_actividad(session: SessionDep, id: int, hard: bool = False):
  if hard:
    eliminar_actividad_hard(session, id)
  else:
    eliminar_actividad_soft(session, id)
  return
