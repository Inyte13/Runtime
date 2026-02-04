import pytest
from fastapi import HTTPException

from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate
from app.services.actividad_service import (
  actualizar_actividad,
  buscar_actividad,
  eliminar_actividad_soft,
  registrar_actividad,
)


def test_registrar_actividad_valida(session_mysql):
  actividad = registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 1"))
  assert actividad.id is not None
  assert actividad.nombre == "actividad 1"


def test_registrar_actividad_duplicada(session_mysql):
  registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 1"))
  with pytest.raises(HTTPException) as exc_info:
    registrar_actividad(session_mysql, ActividadCreate(nombre="actividad 1"))
  assert exc_info.value.status_code == 400
  assert exc_info.value.detail == "Ya existe una actividad con ese nombre"


def test_buscar_actividad_valida(session_mysql):
  actividad = registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 1"))
  assert actividad.id is not None
  actividad_bd = buscar_actividad(session_mysql, actividad.id)
  assert actividad_bd.id == actividad.id
  assert actividad_bd.nombre == "actividad 1"



def test_buscar_actividad_invalida(session_mysql):
  with pytest.raises(HTTPException) as exc_info:
    buscar_actividad(session_mysql, 9999)
  assert exc_info.value.status_code == 404
  assert exc_info.value.detail == "Actividad no encontrada"


def test_actualizar_actividad_nombre_igual(session_mysql):
  actividad = registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 1"))
  actualizado = actualizar_actividad(
    session_mysql, actividad.id, ActividadUpdate(nombre="actividad 1")
  )
  assert actualizado.nombre == "actividad 1"


def test_actualizar_actividad_nombre_duplicado(session_mysql):
  registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 1"))
  actividad2 = registrar_actividad(session_mysql, ActividadCreate(nombre="Actividad 2"))
  with pytest.raises(HTTPException) as exc_info:
    actualizar_actividad(
      session_mysql, actividad2.id, ActividadUpdate(nombre="actividad 1")
    )
  assert exc_info.value.status_code == 400
  assert exc_info.value.detail == "Ya existe una actividad con ese nombre"


def test_eliminar_actividad_soft(session_mysql):
  actividad = registrar_actividad(session_mysql, ActividadCreate(nombre='Actividad 1'))
  eliminar_actividad_soft(session_mysql, actividad.id)
  actividad_bd = buscar_actividad(session_mysql, actividad.id)
  assert actividad_bd.is_active is False
