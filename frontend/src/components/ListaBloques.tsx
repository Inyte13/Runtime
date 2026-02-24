import { Plus } from 'lucide-react'
import { useDiasStore } from '../store/diasStore'
import { BloqueRead } from '../types/Bloque'
import Bloque from './Bloque'
import { Button } from './ui/button'
import { ScrollArea } from './ui/scroll-area'

export default function ListaBloques({ bloques }: {bloques: BloqueRead[]}) {
  const crearBloque = useDiasStore(state => state.crearBloque)

  return (
    <section className='flex flex-col h-full' >
      <ScrollArea className='flex-1 min-h-0 rounded-md border-none px-4'>
        <ul className='flex flex-col gap-y-3'>
          {bloques.map(bloque => (
            <li key={bloque.id}>
              <Bloque bloque={bloque} />
            </li>
          ))}
        </ul>
        <Button className='w-full mt-3'onClick={crearBloque}>
          <Plus />
        </Button>
      </ScrollArea>
    </section>
  )
}
