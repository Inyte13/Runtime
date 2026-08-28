import { BloqueRead } from '@/types/bloque'
import { modificarHora } from './modificarHora'

export function modificarHoras(
  bloques: BloqueRead[],
  indiceRef: number,
  diferencia: number
): BloqueRead[] {
  return bloques.map((bloque, i) => {
    if (i < indiceRef) return bloque
    return {
      ...bloque,
      hora: modificarHora(bloque.hora, diferencia),
      hora_fin: modificarHora(bloque.hora_fin, diferencia),
    }
  })
}
