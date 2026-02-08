import { useActividadesStore } from '../store/actividadesStore.ts'
import './ColorPicker.module.css'

export default function ColorPicker({ bloque, color, setColor }) {
  const actualizarActividad = useActividadesStore((state) => state.actualizarActividad)
  const manejarCambioColor = async (e) => {
    await actualizarActividad(bloque.actividad.id, { color: e.target.value })
  }
  return (
    <input
      type='color'
      value={color}
      style={{ background: color }}
      // onChange solo para cambiar en el frontend
      onChange={(e) => setColor(e.target.value)}
      // onBlur se ejecuta cuando cambia el foco
      onBlur={manejarCambioColor}
    />
  )
}
