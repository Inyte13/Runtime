from sqlmodel import Session

from src.crud.actividad import (
  create_actividad,
  delete_actividad,
  is_exists_bloque,
  read_actividad,
  update_actividad,
)
from src.models.actividad import Actividad
from src.schemas.actividad import (
  ActividadCreate,
  ActividadReadDetail,
  ActividadUpdate,
)


def add_tiene_bloques(
  session: Session, actividad: Actividad
) -> ActividadReadDetail:
  assert actividad.id is not None
  return ActividadReadDetail(
    id=actividad.id,
    nombre=actividad.nombre,
    is_archived=actividad.is_archived,
    tiene_bloques=is_exists_bloque(session, actividad.id),
  )


def validar_actividad(session: Session, id: int) -> None:
  actividad = buscar_actividad(session, id)
  if not actividad.is_archived:
    raise ValueError('La actividad está archivada')


def buscar_actividad(session: Session, id: int) -> Actividad:
  actividad = read_actividad(session, id)
  if not actividad:
    raise ValueError('Actividad no encontrada')
  return actividad


def registrar_actividad(
  session: Session, actividad: ActividadCreate
) -> ActividadReadDetail:
  actividad_detail = create_actividad(
    session, Actividad.model_validate(actividad)
  )
  assert actividad_detail.id is not None
  return ActividadReadDetail(
    id=actividad_detail.id,
    nombre=actividad_detail.nombre,
    is_archived=actividad_detail.is_archived,
    # Si está recién creado el 'tiene_bloques' siempre será False
    tiene_bloques=False,
  )


def actualizar_actividad(
  session: Session, id: int, actividad: ActividadUpdate
) -> Actividad:
  actividad_bd = buscar_actividad(session, id)
  return update_actividad(session, actividad_bd, actividad)


def eliminar_actividad(session: Session, id: int) -> None:
  if is_exists_bloque(session, id):
    raise ValueError(
      'Una actividad con al menos un bloque relacionado no se puede eliminar'
    )
  actividad = buscar_actividad(session, id)
  delete_actividad(session, actividad)
