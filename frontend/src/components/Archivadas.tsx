import { useActividadesStore } from '@/store/actividadesStore'
import { Archive, Search } from 'lucide-react'
import { useShallow } from 'zustand/react/shallow'
import Actividad from './Actividad'
import { memo } from 'react'

export default memo(function Archivadas({ search }: { search: string }) {
  const archivadasIds = useActividadesStore(
    useShallow(state =>
      state.actividadesDetail
        .filter(
          actividad =>
            !actividad.is_active &&
            actividad.nombre.includes(search.toLowerCase())
        )
        .map(actividad => actividad.id)
    )
  )
  return (
    <>
      {archivadasIds.length === 0 ? (
        <div className='h-full flex flex-col items-center justify-center gap-1 text-muted-foreground p-4 border border-border rounded-lg bg-card'>
          {search ? (
            <>
              <Search className='size-4' />
              <p className='text-sm'>Sin resultados</p>
            </>
          ) : (
            <>
              <Archive className='size-4' />
              <p className='text-sm'>Sin actividades archivadas</p>
            </>
          )}
        </div>
      ) : (
        <ul className='flex flex-col divide-y divide-border/50 px-4 flex-1 overflow-y-auto border border-border rounded-lg bg-card text-card-foreground [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none][scrollbar-width:none]'>
          {archivadasIds.map(id => (
            <li className='first:pt-2 last:pb-2' key={id}>
              <Actividad id={id} />
            </li>
          ))}
        </ul>
      )}
    </>
  )
})
