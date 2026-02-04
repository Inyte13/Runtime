from app.crud.actividad_crud import (
  create_actividad,
  delete_actividad,
  read_actividad_by_id,
  read_actividades,
  search_actividad_by_nombre,
  update_actividad,
)
from app.models.actividad import Actividad
from app.schemas.actividad_schema import ActividadUpdate
from app.tests.utils.actividad_util import crear_actividades


def test_create_actividad_nombre(session_sqlite):
  actividad = create_actividad(session_sqlite, Actividad(nombre="Actividad 1"))
  assert actividad.id is not None
  assert actividad.nombre == "Actividad 1"


def test_create_actividad_color(session_sqlite):
  actividad = create_actividad(
    session_sqlite, Actividad(nombre="Actividad 1", color="#234")
  )
  assert actividad.id is not None
  assert actividad.nombre == "Actividad 1"
  assert actividad.color == "#234"


def test_create_actividad_is_active(session_sqlite):
  actividad = create_actividad(
    session_sqlite, Actividad(nombre="Actividad 1", is_active=False)
  )
  assert actividad.id is not None
  assert actividad.nombre == "Actividad 1"
  assert actividad.is_active is False


def test_create_actividad(session_sqlite):
  actividad = create_actividad(
    session_sqlite, Actividad(nombre="Actividad 1", color="#248", is_active=False)
  )
  assert actividad.id is not None
  assert actividad.nombre == "Actividad 1"
  assert actividad.color == "#248"
  assert actividad.is_active is False


def test_read_actividades(session_sqlite):
  actividad1, *demas = crear_actividades(
    session_sqlite, "Actividad 1", "Actividad 2", "Actividad 3"
  )
  update_actividad(session_sqlite, actividad1, ActividadUpdate(is_active=False))
  actividades = read_actividades(session_sqlite)

  assert len(actividades) == 3
  nombres = [act.nombre for act in actividades]

  # assert "Actividad 1" in nombres
  # assert "Actividad 2" in nombres
  # assert "Actividad 3" in nombres
  assert {"Actividad 1", "Actividad 2", "Actividad 3"} <= set(nombres)

  activas = read_actividades(session_sqlite, is_active=True)
  nombres_activas = [act.nombre for act in activas]
  assert "Actividad 1" not in nombres_activas
  assert "Actividad 2" in nombres_activas
  assert "Actividad 3" in nombres_activas

  inactivas = read_actividades(session_sqlite, is_active=False)
  nombres_inactivas = [inac.nombre for inac in inactivas]
  assert "Actividad 1" in nombres_inactivas
  assert "Actividad 2" not in nombres_inactivas
  assert "Actividad 3" not in nombres_inactivas


def test_read_actividad_by_id(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]

  # Si encuentra la actividad
  resultado = read_actividad_by_id(session_sqlite, actividad1.id)
  assert resultado is not None
  assert resultado.nombre == "Actividad 1"
  # Si no encuentra la actividad
  resultado_none = read_actividad_by_id(session_sqlite, 999)
  assert resultado_none is None


def test_search_actividad_by_nombre(session_sqlite):
  crear_actividades(session_sqlite, "Dormir", "Dorar", "Almuerzo")
  # Si hay coincidencias
  actividades = search_actividad_by_nombre(session_sqlite, "Dor")
  buscados = [act.nombre for act in actividades]
  assert "Dormir" in buscados
  assert "Dorar" in buscados
  assert "Almuerzo" not in buscados
  # Si no hay coincidencias
  actividades_sin_match = search_actividad_by_nombre(session_sqlite, "Corr")
  assert actividades_sin_match == []


def test_update_actividad_nombre(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  update_actividad(session_sqlite, actividad1, ActividadUpdate(nombre="Actualizado"))
  # Esperan en lowercase por el validate de ActividadUpdate
  assert actividad1.nombre == "actualizado"


def test_update_actividad_color(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  update_actividad(session_sqlite, actividad1, ActividadUpdate(color="#432"))
  assert actividad1.color == "#432"


def test_update_actividad_is_active(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  update_actividad(session_sqlite, actividad1, ActividadUpdate(is_active=False))
  assert actividad1.is_active is False


def test_update_actividad(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  update = ActividadUpdate(nombre="Actualizado", color="#123", is_active=False)
  update_actividad(session_sqlite, actividad1, update)
  # Esperan en lowercase por el validate de ActividadUpdate
  assert actividad1.nombre == "actualizado"
  assert actividad1.color == "#123"
  assert actividad1.is_active is False


def test_update_actividad_sin_cambios(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  update_actividad(session_sqlite, actividad1, ActividadUpdate())
  assert actividad1.nombre == "Actividad 1"
  assert actividad1.color == "#0191f1"  # Valor por defecto
  assert actividad1.is_active is True  # Valor por defecto


def test_delete_actividad(session_sqlite):
  actividad1 = crear_actividades(session_sqlite, "Actividad 1")[0]
  id = actividad1.id
  delete_actividad(session_sqlite, actividad1)
  eliminado = read_actividad_by_id(session_sqlite, id)
  assert eliminado is None
