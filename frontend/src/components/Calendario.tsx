import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useFechaStore } from '../store/fechaStore.js'
import { Button } from './ui/button.js'

function CalendarioTitle() {
  const FechaTitle = useFechaStore(state => state.getFechaTitle())
  return (
    <>
      <h2>{FechaTitle}</h2>
      <p>Gestiona tus bloques de actividad diaria.</p>
    </>
  )
}

function CalendarioToolbar() {
  const { prevDia, nextDia, irHoy } = useFechaStore()
  return (
    <>
      <div role='group'>
        <Button className=''>Mes</Button>
        <Button className=''>Semana</Button>
      </div>
      <div>
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
    </>
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
