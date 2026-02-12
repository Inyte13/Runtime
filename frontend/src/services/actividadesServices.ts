import { ActividadCreate, ActividadRead, ActividadUpdate } from '../types/Actividad'

const URL = '/actividades'

export async function createActividad(actividad: ActividadCreate): Promise<ActividadRead> {
  const res = await fetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify(actividad)
  })
  if (!res.ok) throw new Error('Error al crear la actividad')
  return res.json() as Promise<ActividadRead>
}

export async function readActividades(isActive?: boolean): Promise<ActividadRead[]> {
  const params = new URLSearchParams()
  if (isActive !== undefined) {
    params.append('is_active', String(isActive))
  }
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok) throw new Error('Error al cargar las actividades')
  return res.json() as Promise<ActividadRead[]>
}

export async function updateActividad(
  id: number,
  actividad: ActividadUpdate
): Promise<ActividadRead> {
  const res = await fetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(actividad)
  })
  if (!res.ok) throw new Error('Error al actualizar la actividad')
  return res.json() as Promise<ActividadRead>
}
