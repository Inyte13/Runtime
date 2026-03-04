import { memo } from 'react'
import ColorPicker from './ColorPicker'
import { useActividadesStore } from '../store/actividadesStore'
import { Input } from './ui/input'
import { manejarEnter } from '../utils/keboard'

// TODO: El primer cambio si renderiza todos los
export default memo(function Actividad({ id }: { id: number }) {
  const nombre = useActividadesStore(
    state =>
      state.actividades.find(actividad => actividad.id === id)?.nombre || ''
  )
  const colorFallback = useActividadesStore(
    state =>
      state.actividades.find(actividad => actividad.id === id)?.color || ''
  )
  return (
    <div className='flex items-center p-1.5 hover:bg-accent hover:text-accent-foreground rounded-lg'>
      <ColorPicker id={id} colorFallback={colorFallback} />
      <span className='capitalize'>{nombre}</span>
    </div>
  )
})
