import { ChevronDown, ChevronUp } from 'lucide-react'
import { Button } from './ui/button'
import { memo } from 'react'
import useDuracionBloque from '@/hooks/useDuracionBloque'
import { useDiasStore } from '@/store/diasStore'

export default memo(function Duracion({ id }: { id: number }) {
  const { manejarDuracion } = useDuracionBloque(id)
  const duracion = useDiasStore(
    state =>
      state.diaDetail?.bloques.find(bloque => bloque.id === id)?.duracion ?? 0
  )
  const nextTime = () => manejarDuracion(duracion + 0.5)
  const prevTime = () => manejarDuracion(Math.max(0, duracion - 0.5))
  return (
    <div data-slot='wrapper' className='flex items-center justify-end'>
      <span className='text-card-foreground text-3xl font-extralight'>
        {duracion}h
      </span>
      <div data-slot='wrapper' className='flex flex-col'>
        <Button
          size='icon-xs'
          onClick={prevTime}
          // TODO: Deberia ser el mínimo múltiplo que elija el usuario ejm(0.25, 0.5, 1)
          disabled={duracion === 0.5}
          variant='ghost'
        >
          <ChevronUp />
        </Button>
        <Button onClick={nextTime} size='icon-xs' variant='ghost'>
          <ChevronDown />
        </Button>
      </div>
    </div>
  )
})
