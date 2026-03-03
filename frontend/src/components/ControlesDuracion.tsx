import { ChevronDown, ChevronUp } from 'lucide-react'
import { Button } from './ui/button'
import { memo } from 'react'

export default memo(function ControlesDuracion({
  duracion,
  manejarDuracion,
  isLast,
}: {
  duracion: number
  manejarDuracion: (newDuracion: number) => void
  isLast: boolean
}) {
  const nextTime = () => isLast && manejarDuracion(duracion + 0.5)
  const prevTime = () => isLast && manejarDuracion(Math.max(0, duracion - 0.5))
  return (
    <div className='flex mr-5 justify-center items-center'>
      <span className='text-3xl font-extralight'>{duracion}h</span>
      <div className='flex flex-col '>
        <Button
          size='icon-xs'
          onClick={prevTime}
          disabled={!isLast || duracion === 0}
          variant='ghost'
        >
          <ChevronUp />
        </Button>
        <Button
          onClick={nextTime}
          size='icon-xs'
          variant='ghost'
          disabled={!isLast}
        >
          <ChevronDown />
        </Button>
      </div>
    </div>
  )
})
