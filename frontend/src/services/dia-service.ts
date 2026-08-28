import { BloqueResponse } from '../types/bloque'
import {
  DiaResponse,
  DiaResponseDetail,
  DiaResumen,
  DiaUpdate,
} from '../types/dia'
import { ApiError } from './errors'

const URL = '/dias'

export async function getDiaDetail(fecha: string): Promise<DiaResponseDetail> {
  const params = new URLSearchParams({
    detail: 'true',
  })
  const res = await fetch(`${URL}/${fecha}?${params.toString()}`)
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a getDiaDetail')
  return res.json()
}

export async function getDiasResumen(
  fechaInicio: string,
  fechaFinal: string
): Promise<DiaResumen[]> {
  const params = new URLSearchParams({
    inicio: fechaInicio,
    final: fechaFinal,
  })
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a getDiasResumen')
  return res.json()
}

export async function updateDia(
  fecha: string,
  dia: DiaUpdate
): Promise<DiaResponse> {
  const res = await fetch(`${URL}/${fecha}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dia),
  })
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a updateDia')
  return res.json()
}

export async function recalculatesHoursDia(
  fecha: string,
  ids: number[]
): Promise<BloqueResponse[]> {
  const res = await fetch(`${URL}/${fecha}/reordenar`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ids),
  })

  if (!res.ok) throw new ApiError(res.status, 'Error haciendo fetch a sortDia')
  return res.json()
}

export async function deleteDia(fecha: string): Promise<void> {
  const res = await fetch(`${URL}/${fecha}`, { method: 'DELETE' })
  if (!res.ok)
    throw new ApiError(res.status, 'Error haciendo fetch a deleteDia')
}
