import { useDiasStore } from '../store/diasStore'
import SelectorActividad from './SelectorActividad'
import { BloqueRead } from '../types/Bloque'
import { XIcon } from 'lucide-react'
import { Button } from './ui/button'
import { memo } from 'react'
import ControlesDuracion from './ControlesDuracion'

export default memo(function BloqueHeader({
  bloque,
  duracion,
  manejarDuracion,
}: {
  bloque: BloqueRead
  duracion: number
  manejarDuracion: (newDuracion: number) => void
}) {
  const eliminarBloque = useDiasStore(state => state.eliminarBloque)
  return (
    <header className='flex justify-between'>
      <SelectorActividad bloque={bloque} />
      <ControlesDuracion
        duracion={duracion}
        manejarDuracion={manejarDuracion}
      />
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
})
