import { useActividadesStore } from '../store/actividadesStore.js'
import { useColorStore } from '../store/colorStore.js'
import { ActividadRead } from '../types/Actividad.js'
export default function ColorPicker({
  actividad,
}: {
  actividad: ActividadRead
}) {
  const color = useColorStore(
    state => state.colores[actividad.id] || actividad.color
  )
  const setColor = useColorStore(state => state.setColor)
  const actualizarActividad = useActividadesStore(
    state => state.actualizarActividad
  )
  const manejarCambioColor = async (e: React.FocusEvent<HTMLInputElement>) => {
    await actualizarActividad(actividad.id, { color: e.target.value })
  }
  return (
    <input
      type='color'
      value={color}
      style={{ background: color }}
      // onChange solo para cambiar en el frontend
      onChange={e => setColor(actividad.id, e.target.value)}
      // onBlur se ejecuta cuando cambia el foco
      onBlur={manejarCambioColor}
    />
  )
}
