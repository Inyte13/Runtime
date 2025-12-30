from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.actividad_crud import (
  create_actividad,
  read_actividad_by_id,
  search_actividad_by_nombre,
  update_actividad,
)
from app.models.actividad import Actividad
from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate


def _validar_nombre_unico(session: Session, nombre: str) -> None:
  if search_actividad_by_nombre(session, nombre):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Ya existe una actividad con ese nombre",
    )
  return


def buscar_actividad(session: Session, id: int) -> Actividad:
  # Leemos la actividad con la fx de actividad_crud, sino existe devuelve None
  actividad = read_actividad_by_id(session, id)
  if not actividad:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada"
    )
  return actividad


def registrar_actividad(session: Session, actividad: ActividadCreate) -> Actividad:
  _validar_nombre_unico(session, actividad.nombre)
  new_actividad = Actividad.model_validate(actividad)
  return create_actividad(session, new_actividad)


def actualizar_actividad(session, id: int, actividad: ActividadUpdate) -> Actividad:
  actividad_bd = buscar_actividad(session, id)
  # Valido si el nombre existe y si es diferente al nombre original
  if actividad.nombre and actividad.nombre != actividad_bd.nombre:
    _validar_nombre_unico(session, actividad.nombre)
  return update_actividad(session, actividad_bd, actividad)


def eliminar_actividad_soft(session: Session, id: int) -> None:
  actividad_bd = buscar_actividad(session, id)
  # Soft delete
  actividad = ActividadUpdate(is_active=False)
  update_actividad(session, actividad_bd, actividad)
  return
