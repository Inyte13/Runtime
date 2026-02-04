const URL = '/bloques'

export async function createBloque (bloque) {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque)
  })
  if (!res.ok) throw new Error('Error al crear el bloque')
  return res.json()
}

export async function updateBloque (id, cambios) {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cambios)
  })
  if (!res.ok) throw new Error('Error al actualizar el bloque')
  return res.json()
}

export async function deleteBloque (id) {
  const res = await fetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error al eliminar el bloque por id')
  // TODO: esperando al backend que retorne algo
}
