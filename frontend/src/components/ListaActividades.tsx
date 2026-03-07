import { useEffect, useState } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import ListaActividadesFooter from './ListaActividadesFooter'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Archive, CircleCheck, X } from 'lucide-react'
import Activas from './Activas'
import Archivadas from './Archivadas'
import { Input } from './ui/input'
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from './ui/input-group'

export default function ListaActividades() {
  const traerActividadesDetail = useActividadesStore(
    state => state.traerActividadesDetail
  )
  const [isCreate, setIsCreate] = useState(false)

  useEffect(() => {
    traerActividadesDetail()
  }, [traerActividadesDetail])
  
  const [search, setSearch] = useState('')
  // TODO: Filtros, por color, con/sin bloques y recientes/semana
  
  // h-auto en lugar de h-9 para evitar salto de layout al cambiar tabs
  return (
    <section className='flex flex-col max-w-60 min-w-60 h-full overflow-hidden p-4 gap-y-2 justify-content'>
      <InputGroup className='w-auto h-auto bg-input/30 border-input/30'>
        <InputGroupInput
          placeholder='Buscar'
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        {search && (
          <InputGroupAddon align='inline-end'>
            <InputGroupButton variant='ghost' size='icon-xs'>
              <X />
            </InputGroupButton>
          </InputGroupAddon>
        )}
      </InputGroup>

      <Tabs defaultValue='activas' className='flex flex-col min-h-0 gap-2'>
        <TabsList className='w-fit'>

          <TabsTrigger value='activas' className='flex gap-1'>
            <CircleCheck className='size-3.5' />
            Activas
          </TabsTrigger>

          <TabsTrigger value='archivadas' className='flex gap-1'>
            <Archive className='size-3.5' />
            Archivadas
          </TabsTrigger>

        </TabsList>

        <TabsContent
          value='activas'
          className='m-0 flex flex-col min-h-50 gap-2'
        >
          <Activas isCreate={isCreate} offCreate={() => setIsCreate(false)} />
          <ListaActividadesFooter onCreate={() => setIsCreate(true)} />
        </TabsContent>

        <TabsContent
          value='archivadas'
          className='m-0 flex flex-col min-h-50 gap-2'
        >
          <Archivadas />
        </TabsContent>
      </Tabs>
    </section>
  )
}
