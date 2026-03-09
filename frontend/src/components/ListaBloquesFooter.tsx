import { memo } from 'react'
import { Button } from './ui/button'
import { Plus } from 'lucide-react'
import { useDiasStore } from '@/store/diasStore'

// Solo para no renderizas el btn cuando use el SelectorActividad
export default memo(function ListaBloquesFooter() {
  const crearBloque = useDiasStore(state => state.crearBloque)
  return (
    <footer className='w-full'>
      <Button size='icon' className='w-full mt-2' onClick={() => crearBloque()}>
        <Plus />
      </Button>
    </footer>
  )
})
