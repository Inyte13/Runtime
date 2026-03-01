import { ChevronDown, ChevronUp } from 'lucide-react'
import { Button } from './ui/button'
import { memo } from 'react'

export default memo(function ControlesDuracion({
  duracion,
  manejarDuracion,
}: {
  duracion: number
  manejarDuracion: (newDuracion: number) => void
}) {
  const nextTime = () => manejarDuracion(duracion + 0.5)
  const prevTime = () => manejarDuracion(Math.max(0, duracion - 0.5))
  return (
    <div className='flex mr-5 justify-center items-center'>
      <span className='text-3xl font-extralight'>{duracion || '0'}h</span>
      <div className='flex flex-col '>
        <Button
          size='icon-xs'
          onClick={prevTime}
          disabled={duracion === 0}
          className={`${duracion === 0 ? '' : ''}`}
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
