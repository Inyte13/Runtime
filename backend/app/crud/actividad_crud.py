from typing import Sequence

from sqlmodel import Session, col, select

from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.schemas.actividad_schema import ActividadUpdate


def create_actividad(session: Session, actividad: Actividad) -> Actividad:
  session.add(actividad)
  session.commit()
  session.refresh(actividad)
  return actividad


# No especifico que devuelvo porque es esto [(Actividad, True), (Actividad, False)])
def read_actividades(session: Session, is_active: bool | None = None):
  subquery = select(Bloque.id).where(Bloque.id_actividad == Actividad.id)
  statement = select(Actividad, subquery.exists())
  if is_active is not None:
    statement = statement.where(Actividad.is_active == is_active)
  return session.exec(statement).all()


def read_actividad_by_id(session: Session, id: int) -> Actividad | None:
  return session.get(Actividad, id)


def search_actividad_by_nombre(
  session: Session, texto_busqueda: str
) -> Sequence[Actividad]:
  patron = f'%{texto_busqueda}%'
  # Buscamos coincidencias insensibles a uppercase y lowercase
  statement = select(Actividad).where(col(Actividad.nombre).ilike(patron))
  return session.exec(statement).all()


def update_actividad(
  session: Session, actividad_bd: Actividad, actividad: ActividadUpdate
) -> Actividad:
  # Convertimos el input a diccionario, excluyendo los nulos
  new_actividad = actividad.model_dump(exclude_unset=True)
  # Actualizamos los atributos
  actividad_bd.sqlmodel_update(new_actividad)
  session.add(actividad_bd)
  session.commit()
  session.refresh(actividad_bd)
  return actividad_bd


def delete_actividad(session: Session, actividad: Actividad) -> None:
  session.delete(actividad)
  session.commit()
