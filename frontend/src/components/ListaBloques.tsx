import { useDiasStore } from '../store/diasStore'
import { BloqueRead } from '../types/Bloque'
import Bloque from './Bloque'
import { Button } from './ui/button'
import { ScrollArea } from './ui/scroll-area'
import { Separator } from './ui/separator'

export default function ListaBloques({ bloques }: { bloques: BloqueRead[] }) {
  const crearBloque = useDiasStore(state => state.crearBloque)
  return (
    <section className='flex flex-col gap-y-4 h-full'>
      <ScrollArea className='flex-1 min-h-0 rounded-md border p-4'>
        <ul>
          {bloques.map((bloque, index) => (
            <li key={bloque.id}>
              <Bloque bloque={bloque} />
              {index < bloques.length - 1 && <Separator className='my-2' />}
            </li>
          ))}
        </ul>
      </ScrollArea>
      <footer className='self-center w-full'>
        <Button onClick={crearBloque} className='w-full'>
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
