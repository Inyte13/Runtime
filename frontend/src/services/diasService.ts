import { DiaRead, DiaReadDetail, DiaUpdate } from '../types/Dia'

const URL = '/dias'

// GET: Dia básico = titulo, estado, fecha
export async function readDia(fecha: string): Promise<DiaRead> {
  const res = await fetch(`${URL}/${fecha}`)
  if (!res.ok) throw new Error('Error al cargar el dia por fecha')
  return res.json() as Promise<DiaRead>
}

// GET: Dia detail = titulo, estado, fecha, bloques
export async function readDiaDetail(fecha: string): Promise<DiaReadDetail> {
  const params = new URLSearchParams({
    detail: 'true',
  })
  const res = await fetch(`${URL}/${fecha}?${params.toString()}`)
  if (!res.ok) throw new Error('Error al cargar el dia detail por fecha')
  return res.json() as Promise<DiaReadDetail>
}

// GET: Dias básicos entre un rango de fechas incluyendo al inicio y al final
// export async function readDiasRange(
//   fechaInicio: string,
//   fechaFinal: string
// ): Promise<DiaRead[]> {
//   const params = new URLSearchParams({
//     inicio: fechaInicio,
//     final: fechaFinal,
//   })
//   const res = await fetch(`${URL}?${params.toString()}`)
//   if (!res.ok) throw new Error('Error al cargar rango de dias por fecha')
//   return res.json() as Promise<DiaRead[]>
// }

// POST? NO, se supone que 'todos' los dias ya están creados solo falta actualizarlos

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
}
