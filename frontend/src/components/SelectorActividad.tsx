import { useActividadesStore } from '@/store/actividadesStore'
import { useDiasStore } from '@/store/diasStore'
import { BloqueRead } from '@/types/Bloque'
import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from './ui/select.js'
import { ActividadRead } from '@/types/Actividad.js'
import SelectorActividadItem from './SelectorActividadItem.js'

export default function SelectorActividad({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const actividades = useActividadesStore(state => state.actividades)

  const manejarSelector = async (actividad: ActividadRead) => {
    await actualizarBloque(bloque.id, { id_actividad: actividad.id })
  }

  const manejarCambio = async (id: string) => {
    const actividad = actividades.find(
      actividad => actividad.id.toString() === id
    )
    if (actividad) manejarSelector(actividad)
  }

  return (
    <Select
      onValueChange={manejarCambio}
      value={bloque.actividad?.id.toString()}
    >
      <SelectTrigger>
        <SelectValue placeholder='Selecciona actividad' />
      </SelectTrigger>
      <SelectContent>
        {actividades.map(actividad => (
          <SelectorActividadItem key={actividad.id} actividad={actividad} />
        ))}
      </SelectContent>
    </Select>
  )
}
