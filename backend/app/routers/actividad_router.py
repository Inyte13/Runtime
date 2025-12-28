from fastapi import APIRouter

from app.core.database import SessionDep
from app.crud.actividad_crud import read_actividades_activas
from app.schemas.actividad_schema import ActividadRead

actividad_router = APIRouter(tags=["Actividades"])


@actividad_router.get("/actividades", response_model=list[ActividadRead])
def get_actividades(session: SessionDep):
  return read_actividades_activas(session)
