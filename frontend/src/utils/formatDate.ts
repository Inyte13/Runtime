// 2026-02-26
export const formatFechaISO = (fecha: Date): string => {
  return fecha.toLocaleDateString('sv-SE')
}

// Febrero 2026
export const formatFechaTitle = (fecha: Date): string => {
  return (
    fecha
      .toLocaleDateString('es-ES', {
        month: 'long',
        year: 'numeric',
      })
      // El primer char a uppercase
      .replace(/^./, c => c.toUpperCase())
      .replace(/ de /g, ' ')
  )
}

// Jueves, 26 feb
export const formatFechaDetail = (fecha: Date): string => {
  return fecha
    .toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'short',
    })
    .replace(/^./, c => c.toUpperCase())
}
