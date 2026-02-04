from app.crud.actividad_crud import create_actividad
from app.models.actividad import Actividad


def crear_actividades(session, *nombres):
  actividades = []
  for nom in nombres:
    actividad = Actividad(nombre=nom)
    create_actividad(session, actividad)
    actividades.append(actividad)
  return actividades
