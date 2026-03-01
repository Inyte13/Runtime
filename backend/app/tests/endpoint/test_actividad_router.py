from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_actividades(client):
  actividad1 = client.post(
    '/actividades', json={'nombre': 'Actividad 1'}
  ).json()
  actividad2 = client.post(
    '/actividades', json={'nombre': 'Actividad 2'}
  ).json()
  actividad3 = client.post(
    '/actividades', json={'nombre': 'Actividad 3'}
  ).json()
  client.delete(f'/actividades/{actividad2["id"]}')

  res = client.get('/actividades')
  assert res.status_code == 200
  actividades = res.json()
  nombres = [actividad['nombre'] for actividad in actividades]
  assert {
    actividad1['nombre'],
    actividad2['nombre'],
    actividad3['nombre'],
  } <= set(nombres)

  res = client.get('/actividades?is_active=true')
  assert res.status_code == 200
  activas = res.json()
  nombres_activas = [actividad['nombre'] for actividad in activas]
  assert actividad1['nombre'] in nombres_activas
  assert actividad2['nombre'] not in nombres_activas
  assert actividad3['nombre'] in nombres_activas
  assert all(actividad['is_active'] for actividad in activas)

  res = client.get('actividades?is_active=false')
  assert res.status_code == 200
  inactivas = res.json()
  nombres_inactivas = [actividad['nombre'] for actividad in inactivas]
  assert actividad1['nombre'] not in nombres_inactivas
  assert actividad2['nombre'] in nombres_inactivas
  assert actividad3['nombre'] not in nombres_inactivas
  assert all(not actividad['is_active'] for actividad in inactivas)


def test_post_actividad_valida(client):
  payload = {'nombre': 'Actividad 1', 'color': '#289', 'is_active': False}
  res = client.post('/actividades', json=payload)
  assert res.status_code == 201
  actividad = res.json()
  assert actividad['nombre'] == 'actividad 1'
  assert actividad['color'] == '#289'
  assert actividad['is_active'] is False
  assert 'id' in actividad


def test_post_actividad_invalida(client):
  res = client.post('/actividades', json={'nombre': ''})
  assert res.status_code == 422


def test_patch_actividad(client):
  payload = {'nombre': 'Actividad 1', 'color': '#289', 'is_active': False}
  actividad = client.post('/actividades', json=payload).json()
  actualizar = {'nombre': 'Actualizar', 'color': '#84f', 'is_active': True}
  res = client.patch(f'/actividades/{actividad["id"]}', json=actualizar)
  assert res.status_code == 200
  actividad = res.json()
  assert actividad['nombre'] == 'actualizar'
  assert actividad['color'] == '#84f'
  assert actividad['is_active'] is True

  actualizar = {'nombre': '', 'color': '', 'is_active': ''}
  res = client.patch(f'/actividades/{actividad["id"]}', json=actualizar)
  assert res.status_code == 422


def test_delete_actividad(client):
  payload = {'nombre': 'Actividad 1', 'color': '#289', 'is_active': True}
  actividad = client.post('/actividades', json=payload).json()
  res = client.delete(f'/actividades/{actividad["id"]}')
  assert res.status_code == 204
  res_get = client.get(f'/actividades/{actividad["id"]}')
  assert res_get.json()['is_active'] is False


def test_delete_actividad_hard(client):
  actividad = client.post('/actividades', json={'nombre': 'Actividad 1'}).json()
  res = client.delete(f'/actividades/{actividad["id"]}/hard')
  assert res.status_code == 204
  res_get = client.get(f'/actividades/{actividad["id"]}')
  assert res_get.status_code == 404
