const URL = '/actividades'
export async function readActividades () {
  const res = await fetch(URL)
  if (!res.ok) throw new Error('Error al cargar las actividades')
  return res.json()
}

export async function updateActividad (id, cambios) {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cambios)
  })
  if (!res.ok) throw new Error('Error al actualizar la actividad')
  return res.json()
}
