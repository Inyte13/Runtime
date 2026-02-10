import { useActividadesStore } from '../store/actividadesStore.js'
import { BloqueRead } from '../types/Bloque.js'
import './ColorPicker.module.css'
interface Props {
  bloque: BloqueRead
  color: string
  setColor: React.Dispatch<React.SetStateAction<string>>
}
export default function ColorPicker({ bloque, color, setColor }: Props) {
  const actualizarActividad = useActividadesStore(
    state => state.actualizarActividad
  )
  const manejarCambioColor = async (e: React.FocusEvent<HTMLInputElement>) => {
    await actualizarActividad(bloque.actividad.id, { color: e.target.value })
  }
  return (
    <input
      type='color'
      value={color}
      style={{ background: color }}
      // onChange solo para cambiar en el frontend
      onChange={e => setColor(e.target.value)}
      // onBlur se ejecuta cuando cambia el foco
      onBlur={manejarCambioColor}
    />
  )
}
