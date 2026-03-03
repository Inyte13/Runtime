import { memo } from 'react'
import ColorPicker from './ColorPicker'
import { useActividadesStore } from '../store/actividadesStore'

// TODO: El primer cambio si renderiza todos los
export default memo(function Actividad({ id }: { id: number }) {
  return (
    <div className='flex items-center gap-2 p-1.5 hover:bg-accent hover:text-accent-foreground cursor-pointer rounded-lg'>
      <ColorPicker actividad={actividad} />
      <span>{nombre}</span>
      <span className='capitalize'>{nombre}</span>
    </div>
  )
})
