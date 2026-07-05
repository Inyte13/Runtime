import {
  CategoriaCreate,
  CategoriaRead,
  CategoriaReadDetail,
  CategoriaUpdate,
} from '@/types/Categoria'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const URL = `${BASE_URL}/categorias`

export async function createCategoria(
  categoria: CategoriaCreate
): Promise<CategoriaReadDetail> {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(categoria),
  })
  if (!res.ok) throw new Error('Error al crear la categoria')
  return res.json()
}

export async function readCategoriasDetail(): Promise<CategoriaReadDetail[]> {
  const res = await fetch(URL)
  if (!res.ok) throw new Error('Error haciendo fetch readCategoriasDetail')
  return res.json()
}

export async function updateCategoria(
  id: number,
  categoria: CategoriaUpdate
): Promise<CategoriaRead> {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(categoria),
  })
  if (!res.ok) throw new Error('Error al actualizar la categoria')
  return res.json()
}

export async function deleteCategoria(id: number): Promise<void> {
  const res = await fetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error al eliminar la categoria')
}
