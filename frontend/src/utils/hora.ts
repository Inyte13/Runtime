export function calcularHoraFin (inicio: string, duracion: number): string {
  // Map number lo convierte a number
  const [hora, minutos] = inicio.split(':').map(Number)
  const totalMinutos = (hora * 60) + minutos + (duracion * 60)
  
  const HH = String(Math.floor(totalMinutos / 60) % 24).padStart(2, '0')
  const MM = String(totalMinutos % 60).padStart(2,'0')
  return `${HH}:${MM}`
}