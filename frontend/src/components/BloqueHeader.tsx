import { useDiasStore } from '../store/diasStore'
import SelectorActividad from './SelectorActividad'
import { BloqueRead } from '../types/Bloque'
import { XIcon } from 'lucide-react'
import { Button } from './ui/button'
import { memo } from 'react'
import ControlesDuracion from './ControlesDuracion'

export default function BloqueHeader({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const eliminarBloque = useDiasStore(state => state.eliminarBloque)
  const [duracion, setDuracion] = useState(bloque.duracion || 0)

  const manejarDuracion = async (newDuracion: number) => {
    setDuracion(newDuracion)
    await actualizarBloque(bloque.id, { duracion: newDuracion })
  }
  const nextTime = () => {
    const newDuracion = duracion + 0.5
    manejarDuracion(newDuracion)
  }
  const prevTime = () => {
    const newDuracion = Math.max(0, duracion - 0.5)
    manejarDuracion(newDuracion)
  }
  return (
    <header className='flex justify-between'>
        <SelectorActividad bloque={bloque} />
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
      <Button
        size='icon-xxs'
        variant='destructive'
        className='top-[0.2rem] right-[0.2rem] absolute'
        onClick={() => eliminarBloque(bloque.id)}
      >
        <XIcon />
      </Button>
    </header>
  )
}
