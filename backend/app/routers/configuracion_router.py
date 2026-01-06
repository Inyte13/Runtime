from app.core.database import SessionDep
from app.schemas.configuracion_schema import DiaDefaultRead, DiaDefaultUpdate
from app.services.configuracion_service import (
  actualizar_configuracion,
  buscar_configuracion,
)
from fastapi import APIRouter

configuracion_router = APIRouter(tags=["Configuracion"])


@configuracion_router.get("/configuracion", response_model=DiaDefaultRead)
def get_configuracion(session: SessionDep):
  return buscar_configuracion(session)


@configuracion_router.patch("/configuracion", response_model=DiaDefaultRead)
def patch_configuracion(session: SessionDep, cambios: DiaDefaultUpdate):
  return actualizar_configuracion(session, cambios)
