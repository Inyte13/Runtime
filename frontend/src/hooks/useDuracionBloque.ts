import { useCallback, useEffect, useRef } from 'react'
import { useDiasStore } from '../store/diasStore'

export default function useDuracionBloque(id: number) {
  const actualizarHoras = useDiasStore(state => state.actualizarHoras)
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const debounceTimer = useRef<number | null>(null)

  const manejarDuracion = useCallback(
    (newDuracion: number) => {
      actualizarHoras(id, newDuracion)
      if (debounceTimer.current) clearTimeout(debounceTimer.current)
      debounceTimer.current = setTimeout(() => {
        actualizarBloque(id, { duracion: newDuracion })
      }, 600)
    },
    [id, actualizarHoras, actualizarBloque]
  )
  // Antes de morir apaga el 600ms
  useEffect(() => {
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current)
    }
  }, [])

  return {
    manejarDuracion,
  }
}
