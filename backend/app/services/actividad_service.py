from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.actividad_crud import (
  create_actividad,
  delete_actividad,
  read_actividad_by_id,
  read_actividades,
  search_actividad_by_nombre,
  update_actividad,
)
from app.models.actividad import Actividad
from app.schemas.actividad_schema import (
  ActividadCreate,
  ActividadReadDetail,
  ActividadUpdate,
)


def _validar_nombre_unico(session: Session, nombre: str) -> None:
  if search_actividad_by_nombre(session, nombre):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Ya existe una actividad con ese nombre',
    )
  return


def buscar_actividad(session: Session, id: int) -> Actividad:
  # Leemos la actividad con la fx de actividad_crud, sino existe devuelve None
  actividad = read_actividad_by_id(session, id)
  if not actividad:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='Actividad no encontrada'
    )
  return actividad


# Especificamos el ActividadReadDetail porque es el único que tiene el atributo tiene_bloques
def mostrar_actividades(
  session: Session, is_active: bool | None = None
) -> Sequence[ActividadReadDetail]:
  # Actividades con el tiene_bloques a lado: [(Actividad, True), (Actividad, False)])
  tuple = read_actividades(session, is_active)
  actividades_detail = []
  for actividad, tiene_bloques in tuple:
    # Lo convertimos en dict
    actividad_detail = actividad.model_dump()
    # Metemos el atributo tiene_bloques
    actividad_detail['tiene_bloques'] = tiene_bloques
    actividades_detail.append(ActividadReadDetail(**actividad_detail))
  return actividades_detail


def registrar_actividad(
  session: Session, actividad: ActividadCreate
) -> Actividad:
  _validar_nombre_unico(session, actividad.nombre)
  new_actividad = create_actividad(session, Actividad.model_validate(actividad))
  actividad_detail = new_actividad.model_dump()
  actividad_detail['tiene_bloques'] = False
  return ActividadReadDetail(**actividad_detail)


def actualizar_actividad(
  session, id: int, actividad: ActividadUpdate
) -> Actividad:
  actividad_bd = buscar_actividad(session, id)
  # Valido si el nombre existe y si es diferente al nombre original
  if actividad.nombre and actividad.nombre != actividad_bd.nombre:
    _validar_nombre_unico(session, actividad.nombre)
  return update_actividad(session, actividad_bd, actividad)


def eliminar_actividad(session: Session, id: int) -> None:
  actividad = buscar_actividad(session, id)
  delete_actividad(session, actividad)
  return
