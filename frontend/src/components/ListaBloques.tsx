import { Plus } from 'lucide-react'
import { useDiasStore } from '../store/diasStore'
import { Button } from './ui/button'
import { memo } from 'react'
import BloqueOrdenable from './BloqueOrdenable'
import { useShallow } from 'zustand/react/shallow'
import {
  DndContext,
  PointerSensor,
  closestCenter,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { restrictToVerticalAxis } from '@dnd-kit/modifiers'

export default memo(function ListaBloques() {
  const bloquesIds = useDiasStore(
    useShallow(
      state => state.diaDetail?.bloques?.map(bloque => bloque.id) ?? []
    )
  )

  return (
        <Button className='w-full mt-2' onClick={crearBloque}>
          <Plus />
        </Button>
    <section className='flex flex-col h-full flex-1 min-h-0 overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]'>
          <ul className='flex flex-col gap-y-2'>
            {bloquesIds.map(id => (
              <BloqueOrdenable key={id} id={id} />
            ))}
          </ul>
    </section>
  )
})
