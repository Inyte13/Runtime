import { useCallback, useEffect, useRef, useState } from 'react'
import { useDiasStore } from '../store/diasStore'
import { calcularHoraFin } from '../utils/hora'

export default function useDuracionBloque(
  id: number,
  duracion: number,
  hora: string
) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const [duracionLocal, setDuracionLocal] = useState(duracion || 0)
  const debounceTimer = useRef<number | null>(null)

  const manejarDuracion = useCallback(
    (newDuracion: number) => {
      setDuracionLocal(newDuracion)
      if (debounceTimer.current) clearTimeout(debounceTimer.current)
      debounceTimer.current = setTimeout(() => {
        actualizarBloque(id, { duracion: newDuracion })
      }, 600)
    },
    [id, actualizarBloque]
  )
  // Antes de morir apaga el 600ms
  useEffect(() => {
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current)
    }
  }, [])

  const horaFin =
    duracionLocal === 0 ? '' : calcularHoraFin(hora, duracionLocal)
  return {
    duracionLocal,
    manejarDuracion,
    horaFin,
  }
}
