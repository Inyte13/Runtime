import { useColorStore } from '@/store/colorStore'
import { ActividadRead } from '@/types/Actividad'
import { SelectItem } from './ui/select'

export default function SelectorActividadItem({
  actividad,
}: {
  actividad: ActividadRead
}) {
  const color = useColorStore(
    state => state.colores[actividad.id] ?? actividad.color
  )

  return (
    <SelectItem value={actividad.id.toString()}>
      <span
        style={{ backgroundColor: color }}
        className='inline-block w-3 h-3 rounded-full mr-1'
      />
      {actividad.nombre.charAt(0).toUpperCase() + actividad.nombre.slice(1)}
    </SelectItem>
  )
}
