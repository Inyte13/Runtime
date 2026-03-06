import { useEffect, useState } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import ListaActividadesFooter from './ListaActividadesFooter'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Archive, CircleCheck } from 'lucide-react'
import Activas from './Activas'
import Archivadas from './Archivadas'
import { Input } from './ui/input'

export default function ListaActividades() {
  const actividadesIds = useActividadesStore(
    useShallow(state => state.actividades.map(actividad => actividad.id))
  )
  const traerActividades = useActividadesStore(state => state.traerActividades)

  const [isCreate, setIsCreate] = useState(false)

  useEffect(() => {
    traerActividades()
  }, [traerActividades])

  return (
    <section className='flex flex-col max-w-60 h-full overflow-hidden p-4 gap-y-2 justify-content'>
      <div className='flex-1 min-h-0 overflow-y-auto border border-border rounded-lg bg-card text-card-foreground [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]'>
        <ul className='flex flex-col divide-y divide-border/50 px-4'>
          {actividadesIds.map(id => (
            <li className='first:pt-2 last:pb-2' key={id}>
              <Actividad id={id} />
            </li>
          ))}
          {isCreate && (
            <li className='first:pt-2 last:pb-2'>
              <ActividadTemp offCreate={() => setIsCreate(false)} />
            </li>
          )}
        </ul>
      </div>
      <ListaActividadesFooter onCreate={() => setIsCreate(true)} />
    </section>
  )
}
