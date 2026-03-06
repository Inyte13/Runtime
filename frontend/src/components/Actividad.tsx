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
  const eliminarActividad = useActividadesStore(
    state => state.eliminarActividad
  )
  if (!actividad) return null
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

  const manejarArchivar = async () => {
    await actualizarActividad(id, { is_active: !actividad.is_active })
  }

  return (
    <div className='group flex items-center p-1.5 rounded-lg'>
      <ColorPicker
        id={id}
        colorFallback={colorFallback}
        disabled={!isArchived}
        className={cn(!isArchived && 'opacity-70')}
      />
      <Input
        className={cn(
          'capitalize p-0 pl-2 border-none outline-none rounded-none h-[1.6rem] text-base',
          !isArchived && 'italic'
        )}
        defaultValue={nombre}
        onBlur={manejarNombre}
        maxLength={50}
        onKeyDown={manejarEnter}
        disabled={!isArchived}
      />

      <Button
        size='icon-xs'
        variant='ghost'
        className='opacity-0 group-hover:opacity-100 transition-none pointer-events-none group-hover:pointer-events-auto'
        onClick={manejarArchivar}
      >
        {actividad.is_active ? <Archive /> : <ArchiveRestore />}
      </Button>
      {!tiene_bloques && (
        <Button
          size='icon-xs'
          variant='destructive'
          className='opacity-0 group-hover:opacity-100 transition-none pointer-events-none group-hover:pointer-events-auto'
          onClick={() => eliminarActividad(id)}
        >
          <Trash2 />
        </Button>
      )}
    </div>
  )
})
