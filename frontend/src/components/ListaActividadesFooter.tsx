import { memo } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import { Button } from './ui/button'
import { Plus } from 'lucide-react'

// Solo para no renderizas el btn cuando use el SelectorActividad
export default memo(function ListaActividadesFooter() {
  const crearActividad = useActividadesStore(state => state.crearActividad)

  return (
    <footer className='w-full'>
      <Button
        size='icon-md'
        className='w-full'
        onClick={
          () =>
            crearActividad({
              nombre: 'Test',
              color: '#ff0000',
              is_active: true,
            })
          // TODO: Crear menu para crear actividad
        }
      >
        <Plus />
      </Button>
    </footer>
  )
})
