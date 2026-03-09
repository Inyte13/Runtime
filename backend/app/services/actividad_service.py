from sqlmodel import Session

from app.crud.actividad_crud import (
  delete_actividad,
  is_exists_bloque,
  read_actividad,
  read_actividades,
  update_actividad,
)
from app.models.actividad import Actividad
from app.schemas.actividad_schema import (
  ActividadReadDetail,
  ActividadUpdate,
)


def buscar_actividad(session: Session, id: int) -> Actividad:
  actividad = read_actividad(session, id)
  if not actividad:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='Actividad no encontrada'
    )
  return actividad


def mostrar_actividades(
  session: Session, is_active: bool | None = None
) -> list[ActividadReadDetail]:
  actividades = read_actividades(session, is_active)
  return [
    ActividadReadDetail(
      **actividad.model_dump(),
      # actividad.id nunca sera none por mi backend
      tiene_bloques=is_exists_bloque(session, actividad.id),  # type: ignore
    )
    for actividad in actividades
  ]


def actualizar_actividad(
  session, id: int, actividad: ActividadUpdate
) -> Actividad:
  actividad_bd = buscar_actividad(session, id)
  return update_actividad(session, actividad_bd, actividad)


def eliminar_actividad(session: Session, id: int) -> None:
  actividad = buscar_actividad(session, id)
  delete_actividad(session, actividad)
