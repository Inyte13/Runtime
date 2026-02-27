import { DiaCreate, DiaRead, DiaReadDetail, DiaUpdate } from '../types/Dia'

const URL = '/dias'

export async function createDia(dia: DiaCreate): Promise<DiaRead> {
  const res = await fetch(`${URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dia),
  })
  if (!res.ok) throw new Error('Error al crear el día')
  return res.json() as Promise<DiaRead>
}
export async function readDia(fecha: string): Promise<DiaRead> {
  const res = await fetch(`${URL}/${fecha}`)
  if (!res.ok) throw new Error('Error al cargar el dia por fecha')
  return res.json() as Promise<DiaRead>
}

export async function readDiaDetail(fecha: string): Promise<DiaReadDetail> {
  const res = await fetch(`${URL}/${fecha}/detail`)
  if (!res.ok) throw new Error('Error al cargar el dia detail por fecha')
  return res.json() as Promise<DiaReadDetail>
}

export async function readDiaRange(
  fechaInicio: string,
  fechaFinal: string
): Promise<DiaRead[]> {
  const params = new URLSearchParams({
    fecha_inicio: fechaInicio,
    fecha_final: fechaFinal,

  })
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok) throw new Error('Error al cargar rango de dias por fecha')
  return res.json() as Promise<DiaRead[]>
}


export async function updateDia(
  fecha: string,
  dia: DiaUpdate
): Promise<DiaRead> {
  const res = await fetch(`${URL}/${fecha}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dia),
  })
  if (!res.ok) throw new Error('Error al actualizar el dia')
  return res.json() as Promise<DiaRead>
}

export async function deleteDia(fecha: string): Promise<void> {
  const res = await fetch(`${URL}/${fecha}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error al eliminar el día por fecha')
  // TODO: esperamos que el backend retorne algo
}
