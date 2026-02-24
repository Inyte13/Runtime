import { useEffect } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import Actividad from './Actividad'
import { Plus } from 'lucide-react'
import { Button } from './ui/button'
import { ScrollArea } from './ui/scroll-area'

export default function ListaActividades() {
  const actividades = useActividadesStore(state => state.actividades)
  const traerActividades = useActividadesStore(state => state.traerActividades)
  useEffect(() => {
    traerActividades()
  }, [traerActividades])

  const crearActividad = useActividadesStore(state => state.crearActividad)
  return (
    <section className='flex flex-col h-full overflow-hidden p-4 gap-y-4 justify-content'>
      <ScrollArea className='flex-1 min-h-0 border border-border rounded-lg bg-card text-card-foreground'>
        <ul className='flex flex-col divide-y divide-border/30 px-4'>
          {actividades.map(actividad => (
            <li className='first:pt-2 last:pb-2' key={actividad.id}>
              <Actividad actividad={actividad} />
            </li>
          ))}
        </ul>
      </ScrollArea>
      <footer className='w-full' >
        <Button
          size='icon-md'
          className='w-full'
          onClick={
            () =>
              crearActividad({ nombre: 'Test', color: 'red', is_active: true })
            // TODO: Crear menu para crear actividad
          }
        >
          <Plus />
        </Button>
      </footer>
    </section>
  )
}
