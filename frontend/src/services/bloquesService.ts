import { BloqueCreate, BloqueRead, BloqueUpdate } from '../types/Bloque'

const URL = '/bloques'

export async function createBloque(bloque: BloqueCreate): Promise<BloqueRead> {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque)
  })
  if (!res.ok) throw new Error('Error al crear el bloque')
  return res.json() as Promise<BloqueRead>
}

export async function updateBloque(id: number, bloque: BloqueUpdate): Promise<BloqueRead> {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque)
  })
  if (!res.ok) throw new Error('Error al actualizar el bloque')
  return res.json() as Promise<BloqueRead>
}

export async function deleteBloque(id: number): Promise<void> {
  const res = await fetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error al eliminar el bloque por id')
  // TODO: esperando al backend que retorne algo
}
