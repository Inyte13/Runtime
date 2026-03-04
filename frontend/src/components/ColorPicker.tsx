import { useActividadesStore } from '../store/actividadesStore.js'
import { useColorStore } from '../store/colorStore.js'

export default function ColorPicker({
  id,
  colorFallback,
}: {
  id: number
  colorFallback: string
}) {
  const color = useColorStore(state => state.colores[id] || colorFallback)
  const setColor = useColorStore(state => state.setColor)
  const actualizarActividad = useActividadesStore(
    state => state.actualizarActividad
  )
  const manejarCambioColor = async (e: React.FocusEvent<HTMLInputElement>) => {
    await actualizarActividad(id, { color: e.target.value })
  }
  return (
    <input
      className='rounded-full size-4'
      style={{ background: color }}
      type='color'
      value={color}
      onChange={e => setColor(id, e.target.value)}
      onBlur={manejarCambioColor}
    />
  )
}
