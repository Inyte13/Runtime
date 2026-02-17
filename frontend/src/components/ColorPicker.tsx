import { useState, useRef } from 'react'
import { useActividadesStore } from '../store/actividadesStore.js'
import { useColorStore } from '../store/colorStore.js'
import { ActividadRead } from '../types/Actividad.js'

export default function ColorPicker({
  actividad,
}: {
  actividad: ActividadRead
}) {
  const [colorTemp, setColorTemp] = useState<string | null>(null)
  const timeoutRef = useRef<number | null>(null)

  const color = useColorStore(
    state => state.colores[actividad.id] || actividad.color
  )
  const setColor = useColorStore(state => state.setColor)
  const actualizarActividad = useActividadesStore(
    state => state.actualizarActividad
  )

  const manejarCambio = (e: React.ChangeEvent<HTMLInputElement>) => {
    const nuevoColor = e.target.value
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
    timeoutRef.current = setTimeout(() => {
      setColor(actividad.id, nuevoColor)
    }, 100)
    setColorTemp(nuevoColor)
  }

  const manejarBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    actualizarActividad(actividad.id, { color: e.target.value })
    setColorTemp(null)
  }

  const displayColor = colorTemp !== null ? colorTemp : color

  return (
    <input
      className='rounded-full w-4 h-4'
      type='color'
      value={displayColor}
      style={{ background: displayColor }}
      onChange={manejarCambio}
      onBlur={manejarBlur}
    />
  )
}
