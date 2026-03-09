import Bloque from './Bloque'
import { memo } from 'react'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { Button } from './ui/button'
import { GripVertical, Plus } from 'lucide-react'
import { useDiasStore } from '@/store/diasStore'

// Creado solo para separar el li del bloque y dejarlo limpio
export default memo(function BloqueOrdenable({
  id,
  idPrevious,
}: {
  id: number
  idPrevious: number
}) {
  const crearBloque = useDiasStore(state => state.crearBloque)
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id })

  // Son las coordenadas exactas para que el bloque persiga a tu ratón
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <li
      ref={setNodeRef} // El contenedor que se movera
      style={style}
      className='group/bloque list-none w-full relative'
    >
      <Bloque id={id} />
      <div className='absolute right-[-1.7rem] top-0 h-full flex flex-col items-center justify-center opacity-0 group-hover/bloque:opacity-80 transition-opacity'>
        <Button
          size='icon-sm'
          variant='ghost'
          className='cursor-grab active:cursor-grabbing w-6 h-7'
          {...attributes}
          {...listeners}
        >
          <GripVertical />
        </Button>
        <Button
          size='icon-sm'
          variant='ghost'
          className='w-6 h-7'
          onClick={e => (e.altKey ? crearBloque(idPrevious ?? 0) : crearBloque(id))}
        >
          <Plus />
        </Button>
      </div>
    </li>
  )
})
