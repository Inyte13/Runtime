import { useEffect } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import Actividad from './Actividad'
import ListaActividadesFooter from './ListaActividadesFooter'

export default function ListaActividades() {
  const actividades = useActividadesStore(state => state.actividades)
  const traerActividades = useActividadesStore(state => state.traerActividades)

  useEffect(() => {
    traerActividades()
  }, [traerActividades])

  return (
    <section className='flex flex-col h-full overflow-hidden p-4 gap-y-2 justify-content'>
      <div className='flex-1 min-h-0 overflow-y-auto border border-border rounded-lg bg-card text-card-foreground [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]'>
        <ul className='flex flex-col divide-y divide-border/30 px-4'>
          {actividades.map(actividad => (
            <li className='first:pt-2 last:pb-2' key={actividad.id}>
              <Actividad actividad={actividad} />
            </li>
          ))}
        </ul>
      </div>
      <ListaActividadesFooter />
    </section>
  )
}
