const URL = '/dias'

export async function createDia (dia) {
  const res = await fetch(`${URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dia)
  })
  if (!res.ok) throw new Error('Error al crear el día')
  return res.json()
}

export async function readDiaDetail (fecha) {
  const res = await fetch(`${URL}/${fecha}`)
  if (!res.ok) throw new Error('Error al cargar el dia por fecha')
  return res.json()
}

export async function readDiaRange (fechaInicio, fechaFinal) {
  const params = new URLSearchParams({
    fecha_inicio: fechaInicio,
    fecha_final: fechaFinal
  })
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok) throw new Error('Error al cargar rango de dias por fecha')
  return res.json()
}

export async function updateDia (fecha, cambios) {
  const res = await fetch(`${URL}/${fecha}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cambios)
  })
  if (!res.ok) throw new Error('Error al actualizar el dia')
  return res.json()
}

export async function deleteDia (fecha) {
  const res = await fetch(`${URL}/${fecha}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Error al eliminar el día por fecha')
  // TODO: esperamos que el backend retorne algo
}
