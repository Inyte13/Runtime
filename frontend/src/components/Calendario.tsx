import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useFechaStore } from '../store/fechaStore.js'
import { Button } from './ui/button.js'
import { formatFechaTitle } from '../utils/formatDate.js'

function CalendarioTitle() {
  const FechaTitle = useFechaStore(state => state.getFechaTitle())
  return (
    <>
      <h2 className='text-2xl font-semibold'>{FechaTitle}</h2>
      <p>Gestiona tus bloques de actividad diaria.</p>
    </>
  )
}

function CalendarioToolbar() {
  const { prevDia, nextDia, irHoy } = useFechaStore()
  return (
    <div className='flex'>
      <div >
        <Button className=''>Mes</Button>
        <Button className=''>Semana</Button>
      </div>
      <div className='flex'>
        <Button size='icon-md' className='' onClick={prevDia}>
          <ChevronLeft />
        </Button>
        <Button className='' onClick={irHoy}>
          Hoy
        </Button>
        <Button size='icon-md' className='' onClick={nextDia}>
          <ChevronRight />
        </Button>
      </div>
    </div>
  )
}

export default function Calendario() {
  return (
    <header className='p-4'>
      <CalendarioTitle />
      <CalendarioToolbar />
    </header>
  )
}
