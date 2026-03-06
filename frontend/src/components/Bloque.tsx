import { useDiasStore } from '../store/diasStore'
import BloqueHeader from './BloqueHeader'
import { Input } from './ui/input'
import { memo, useCallback } from 'react'
import useDuracionBloque from '../hooks/useDuracionBloque'
import BloqueColor from './BloqueColor'
import { manejarEnter } from '../utils/keyboard'
import { Button } from './ui/button'
import { GripVertical, X } from 'lucide-react'
import { DraggableAttributes } from '@dnd-kit/core'
import { SyntheticListenerMap } from '@dnd-kit/core/dist/hooks/utilities'

export default memo(function Bloque({
  id,
  attributes,
  listeners,
}: {
  id: number
  attributes: DraggableAttributes
  listeners?: SyntheticListenerMap
}) {
  const bloque = useDiasStore(state =>
    state.diaDetail?.bloques.find(bloque => bloque.id === id)
  )
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const eliminarBloque = useDiasStore(state => state.eliminarBloque)

  const { manejarDuracion } = useDuracionBloque(id)

  const descripcion = bloque?.descripcion || ''
  const manejarDescripcion = useCallback(
    async (e: React.FocusEvent<HTMLInputElement>) => {
      const newDescripcion = e.target.value
      if (newDescripcion === descripcion) return
      await actualizarBloque(id, { descripcion: e.target.value })
    },
    [id, descripcion, actualizarBloque]
  )
  if (!bloque) return null
  return (
    <BloqueColor
      id={bloque.actividad.id}
      colorDefault={bloque.actividad.color}
      className='group flex flex-col border border-border border-l-2 rounded-md px-2 pb-2 pt-1 relative bg-card w-full'
    >
      <BloqueHeader
        id={id}
        duracion={bloque.duracion || 0}
        manejarDuracion={manejarDuracion}
      />

      <Button
        size='icon-xs'
        variant='ghost'
        className='top-[0.2rem] right-[0.2rem] absolute opacity-0 group-hover:opacity-100 focus-visible:opacity-100'
        onClick={() => eliminarBloque(id)}
      >
        <X />
      </Button>

      <div
        // El handle, el unico receptor del agarre
        {...attributes}
        {...listeners}
        className='absolute top-1/2 -translate-y-1/2 right-0 z-10 cursor-grab active:cursor-grabbing opacity-30 hover:opacity-100 transition-opacity'
      >
        <GripVertical />
      </div>

      <span className='pl-1 text-foreground/70'>
        {bloque.hora} {(bloque.duracion ?? 0) > 0 && `- ${bloque.hora_fin}`}
      </span>

      <Input
        className='border-0 border-b border-transparent focus:border-(--color) outline-none rounded-none italic h-[1.6rem] text-base pr-0 pl-1 mt-1'
        defaultValue={descripcion}
        placeholder='Añadir descripción'
        onBlur={manejarDescripcion}
        maxLength={255}
        onKeyDown={manejarEnter}
      />
    </BloqueColor>
  )
})
