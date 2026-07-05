import { BloqueRead } from '../types/Bloque'
import { DiaRead, DiaReadDetail, DiaResumen, DiaUpdate } from '../types/Dia'

const BASE_URL = import.meta.env.VITE_API_URL || ''
const URL = `${BASE_URL}/dias`

export async function readDiaDetail(fecha: string): Promise<DiaReadDetail> {
  const params = new URLSearchParams({
    detail: 'true',
  })
  const res = await fetch(`${URL}/${fecha}?${params.toString()}`)
  if (!res.ok) throw new Error('Error haciendo fetch a readDiaDetail')
  return res.json()
}

export async function readDiasResumen(
  fechaInicio: string,
  fechaFinal: string
): Promise<DiaResumen[]> {
  const params = new URLSearchParams({
    inicio: fechaInicio,
    final: fechaFinal,
  })
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok) throw new Error('Error haciendo fetch a readDiasResumen')
  return res.json()
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
  if (!res.ok) throw new Error('Error haciendo fetch a updateDia')
  return res.json()
}

export async function sortDia(
  fecha: string,
  ids: number[]
): Promise<BloqueRead[]> {
  const res = await fetch(`${URL}/${fecha}/reordenar`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ids),
  })

  if (!res.ok) throw new Error('Error haciendo fetch a sortDia')
  return res.json()
}

export async function deleteDia(fecha: string): Promise<void> {
  const res = await fetch(`${URL}/${fecha}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error haciendo fetch a deleteDia')
}
