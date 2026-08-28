import { ChevronLeft, ChevronRight, Menu, Moon, Sun } from 'lucide-react'
import { useFechaStore } from '../store/fechaStore.js'
import { Button } from './ui/button.js'
import { formatFechaTitle } from '../utils/formatDate.js'
import { useDiasStore } from '@/store/diasStore.js'
import Calendario from './Calendario.js'
import Sidebar from './Sidebar.js'
import { useEffect, useState } from 'react'
import { cn } from '@/lib/utils.js'

export default function Layout() {
  const { prevDia, nextDia, irHoy, prevMes, nextMes } = useFechaStore()
  const fecha = useFechaStore(state => state.fecha)
  const fechaTitle = formatFechaTitle(fecha)

  const traerDiasResumen = useDiasStore(state => state.traerDiasResumen)
  useEffect(() => {
    traerDiasResumen()
  }, [traerDiasResumen])

  const [sidebarOpen, setSidebarOpen] = useState(true)

  // Btn para dark mode
  const [isDark, setIsDark] = useState(
    () => localStorage.getItem('theme') === 'dark'
  )
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }, [isDark])
  return (
    <section className='flex flex-col w-full h-full gap-y-3 p-4 pl-0'>
      <header className='flex gap-x-2 justify-between items-center pl-4'>
        <Button
          size='icon-sm'
          variant='ghost'
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <Menu />
        </Button>
        <div
          data-slot='wrapper'
          className='flex gap-2 items-center justify-between flex-1 min-w-80 max-w-80'
        >
          <Button
            size='icon'
            variant='ghost'
            className='rounded-full'
            onClick={prevMes}
          >
            <ChevronLeft />
          </Button>
          <h2 className='text-3xl font-semibold'>{fechaTitle}</h2>
          <Button
            size='icon'
            variant='ghost'
            className='rounded-full'
            onClick={nextMes}
          >
            <ChevronRight />
          </Button>
        </div>

        <div data-slot='wrapper' className='flex items-center gap-x-1'>
          <Button
            size='icon-sm'
            variant='ghost'
            onClick={() => setIsDark(!isDark)}
          >
            {isDark ? <Sun /> : <Moon />}
          </Button>

          <Button
            size='icon'
            variant='secondary'
            className='rounded-full'
            onClick={prevDia}
          >
            <ChevronLeft />
          </Button>
          <Button variant='secondary' onClick={irHoy}>
            Hoy
          </Button>
          <Button
            size='icon'
            variant='secondary'
            className='rounded-full'
            onClick={nextDia}
          >
            <ChevronRight />
          </Button>
        </div>
      </header>
      <main className='flex w-full min-h-0 flex-1 gap-x-4'>
        <div
          data-component='wrapper'
          className={cn(
            'overflow-hidden transition-[width] duration-300 ease-in-out h-full shrink-0',
            sidebarOpen ? 'w-56' : 'w-0'
          )}
        >
          <Sidebar />
        </div>
        <Calendario />
      </main>
    </section>
  )
}
