from fastapi import APIRouter

from app.core.database import SessionDep
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
  registrar_actividad,
)

actividad_router = APIRouter(tags=['Actividades'])


# GET: Todas las actividades, puede ser None para traer activos e inactivos
@actividad_router.get('/actividades', response_model=list[ActividadReadDetail])
def get_actividades(session: SessionDep, is_active: bool | None = None):
  return mostrar_actividades(session, is_active)


@actividad_router.post(
  '/actividades', status_code=201, response_model=ActividadReadDetail
)
def post_actividad(session: SessionDep, actividad: ActividadCreate):
  return registrar_actividad(session, actividad)


@actividad_router.patch('/actividades/{id}', response_model=ActividadRead)
def patch_actividad(session: SessionDep, actividad: ActividadUpdate, id: int):
  return actualizar_actividad(session, id, actividad)


@actividad_router.delete('/actividades/{id}', status_code=204)
def delete_actividad(session: SessionDep, id: int):
  eliminar_actividad(session, id)
  return
