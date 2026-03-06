import { memo } from 'react'
import { Button } from './ui/button'
import { Plus } from 'lucide-react'

// Solo para no renderizas el btn cuando use el SelectorActividad
export default memo(function ListaActividadesFooter({onCreate}: {onCreate: () => void}) {
  return (
    <footer className='w-full'>
      <Button size='icon' className='w-full' onClick={onCreate}>
        <Plus />
      </Button>
    </footer>
  )
})
