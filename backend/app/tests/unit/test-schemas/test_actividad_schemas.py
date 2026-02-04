import pytest

from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate


def test_create_nombre_vacio():
  # Si lanza exception 'ValueError', el test pasa
  with pytest.raises(ValueError):
    ActividadCreate(nombre="")


def test_create_nombre_espacios():
  with pytest.raises(ValueError):
    ActividadCreate(nombre="   ")


def test_create_nombre_lowercase():
  act = ActividadCreate(nombre="Actividad 1")
  assert act.nombre == "actividad 1"


def test_update_nombre_none():
  act = ActividadUpdate(nombre=None)
  assert act.nombre is None  # se permite None


def test_update_nombre_vacio():
  with pytest.raises(ValueError):
    ActividadUpdate(nombre="")


def test_update_nombre_espacios():
  with pytest.raises(ValueError):
    ActividadUpdate(nombre="   ")


def test_update_nombre_lowercase():
  act = ActividadUpdate(nombre="Actividad 1")
  assert act.nombre == "actividad 1"


def test_create_color_vacio():
  with pytest.raises(ValueError):
    ActividadCreate(nombre='Actividad 1', color='')

  
def test_create_color_valido():
  act = ActividadCreate(nombre='Actividad 1', color='#f23')
  assert act.color == '#f23'


def test_update_color_none():
  act = ActividadUpdate(color=None)
  assert act.color is None


def test_update_color_vacio():
  with pytest.raises(ValueError):
    ActividadUpdate(color='')


def test_update_color_valido():
  act = ActividadUpdate(color='#423')
  assert act.color == '#423'