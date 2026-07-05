import { BloqueCreate, BloqueRead, BloqueUpdate } from '../types/Bloque'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const URL = `${BASE_URL}/bloques`

export async function createBloque(bloque: BloqueCreate): Promise<BloqueRead> {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque),
  })
  if (!res.ok) throw new Error('Error haciendo fetch a createBloque')
  return res.json()
}

export async function updateBloque(
  id: number,
  bloque: BloqueUpdate
): Promise<BloqueRead> {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque),
  })
  if (!res.ok) throw new Error('Error haciendo fetch a updateBloque')
  return res.json()
}

export async function deleteBloque(id: number): Promise<void> {
  const res = await fetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error haciendo fetch a deleteBloque')
}
