import { useEffect } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import Actividad from './Actividad'
import { ScrollArea } from './ui/scroll-area'
import { Button } from './ui/button'
import { Separator } from './ui/separator'

export default function ListaActividades() {
  const actividades = useActividadesStore(state => state.actividades)
  const traerActividades = useActividadesStore(state => state.traerActividades)
  useEffect(() => {
    traerActividades()
  }, [traerActividades])

  const crearActividad = useActividadesStore(state => state.crearActividad)
  return (
    <section className='flex flex-col gap-y-4 h-full'>
      <ScrollArea className='flex-1 min-h-0 min-w-52 rounded-md border p-4'>
        <ul>
          {actividades.map((actividad, index) => (
            <li
              key={actividad.id}
            >
              <Actividad actividad={actividad} />
              {index < actividades.length - 1 && <Separator className='my-2' />}
            </li>
          ))}
        </ul>
      </ScrollArea>
      <footer className='self-center w-full'>
        <Button
          className='w-full'
          onClick={() =>
            crearActividad({
              nombre: 'Nueva actividad',
              color: '#000000',
              is_active: true,
              // TODO: Crear una forma para crear la actividad deseada
            })
          }
        >
          <svg
            xmlns='http://www.w3.org/2000/svg'
            width='24'
            height='24'
            viewBox='0 0 24 24'
            fill='none'
            stroke='currentColor'
            strokeWidth='2'
            strokeLinecap='round'
            strokeLinejoin='round'
            className='icon icon-tabler icons-tabler-outline icon-tabler-plus'
          >
            <path stroke='none' d='M0 0h24v24H0z' fill='none' />
            <path d='M12 5l0 14' />
            <path d='M5 12l14 0' />
          </svg>
        </Button>
      </footer>
    </section>
  )
}
