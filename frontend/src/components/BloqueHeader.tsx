import Duracion from './Duracion'
import SelectorActividad from './SelectorActividad'
import { memo } from 'react'

export default memo(function BloqueHeader({
  id,
  duracion,
  manejarDuracion,
}: {
  id: number
  duracion: number
  manejarDuracion: (newDuracion: number) => void
}) {
  return (
    <header className='flex justify-between'>
      <SelectorActividad id={id} />
      <Duracion duracion={duracion} manejarDuracion={manejarDuracion} />
    </header>
  )
})
