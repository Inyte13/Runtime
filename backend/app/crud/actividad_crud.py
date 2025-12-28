from typing import Sequence

from sqlmodel import Session, col, select

from app.models.actividad import Actividad


# Sequence, una lista solo de lectura
def read_actividades(
  session: Session,
) -> Sequence[Actividad]:
  statement = select(Actividad)
  return session.exec(statement).all()


def read_actividades_activas(session: Session) -> Sequence[Actividad]:
  statement = select(Actividad).where(Actividad.is_active)
  return session.exec(statement).all()


def read_actividad_by_id(session: Session, actividad_id: int) -> Actividad | None:
  return session.get(Actividad, actividad_id)


def read_actividad_by_nombre(session: Session, nombre: str) -> Actividad | None:
  statement = select(Actividad).where(Actividad.nombre == nombre)
  return session.exec(statement).first()


def search_actividad_by_nombre(
  session: Session, texto_busqueda: str
) -> Sequence[Actividad]:
  patron = f"%{texto_busqueda}%"
  # Buscamos coincidencias insensibles a uppercase y lowercase
  statement = select(Actividad).where(col(Actividad.nombre).ilike(patron))
  return session.exec(statement).all()


def create_actividad(session: Session, actividad: Actividad) -> Actividad:
  session.add(actividad)
  session.commit()
  session.refresh(actividad)
  return actividad
