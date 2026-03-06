import { memo } from 'react'
import ColorPicker from './ColorPicker'
import { useActividadesStore } from '../store/actividadesStore'
import { Input } from './ui/input'
import { manejarEnter } from '../utils/keyboard'
import { Button } from './ui/button'
import { Archive, ArchiveRestore, Trash2 } from 'lucide-react'
import { cn } from '@/lib/utils'

// TODO: El primer cambio si renderiza todos los
export default memo(function Actividad({ id }: { id: number }) {
  const actividad = useActividadesStore(state =>
    state.actividadesDetail.find(actividad => actividad.id === id)
  )
  const actualizarActividad = useActividadesStore(
    state => state.actualizarActividad
  )
  const { nombre, color: colorFallback, tiene_bloques } = actividad

  const manejarNombre = async (e: React.FocusEvent<HTMLInputElement>) => {
    const newNombre = e.target.value.toLowerCase().trim()
    // Si el newNombre es '' o es igual al inicial
    if (!newNombre || newNombre === nombre) {
      e.target.value = nombre
      return
    }
    await actualizarActividad(id, { nombre: newNombre })
  }
  // TODO: Todavia no se agrego el lugar de la papelera para incluir el soft
  const eliminarActividad = useActividadesStore(
    state => state.eliminarActividad
  )

  return (
    <div className='flex items-center p-1.5 hover:bg-accent hover:text-accent-foreground rounded-lg'>
      <ColorPicker id={id} colorFallback={colorFallback} />
      <Input
        className='capitalize p-0 pl-2 border-none outline-none rounded-none h-[1.6rem] text-base'
        defaultValue={nombre}
        onBlur={manejarNombre}
        maxLength={50}
        onKeyDown={manejarEnter}
      />
    </div>
  )
})
