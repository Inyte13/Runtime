import { BloqueCreate, BloqueResponse, BloqueUpdate } from '../types/bloque'
import { apiClient } from './api-client';
import { ApiError } from './errors'

const URL = '/bloques'

export async function createBloque(
  bloque: BloqueCreate
): Promise<BloqueResponse> {
  return apiClient<BloqueResponse>(URL, {
    method: 'POST',
    body: JSON.stringify(bloque)
  })
}

export async function updateBloque(
  id: number,
  bloque: BloqueUpdate
): Promise<BloqueResponse> {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bloque),
  })
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a updateBloque')
  return res.json()
}

export async function deleteBloque(id: number): Promise<void> {
  const res = await fetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a deleteBloque')
}
