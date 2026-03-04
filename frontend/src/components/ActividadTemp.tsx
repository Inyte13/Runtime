import { useEffect, useRef, useState } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import { Input } from './ui/input'
import { manejarEnter } from '../utils/keyboard'

export default function ActividadTemp({
  offCreate,
}: {
  offCreate: () => void
}) {
  const crearActividad = useActividadesStore(state => state.crearActividad)

  const tempRef = useRef<HTMLDivElement>(null)

  const [nombreTemp, setNombreTemp] = useState('')
  // Si lo cambias también lo tienes que hacer en el backend (actividad.py)
  const [colorTemp, setColorTemp] = useState('#0191f1')

  // Auto-scroll cuando se crea el holograma de Actividad
  useEffect(() => {
    tempRef.current?.scrollIntoView({ behavior: 'auto', block: 'end' })
  }, [])

  const actualizar = async () => {
    const nombre = nombreTemp.trim()
    if (nombre) {
      await crearActividad({ nombre: nombre.toLowerCase(), color: colorTemp })
    }
    offCreate()
  }

  const manejarBlur = (e: React.FocusEvent<HTMLDivElement>) => {
    // Si el nuevo elemento clickeado está fuera, guardamos
    if (!e.currentTarget.contains(e.relatedTarget)) {
      actualizar()
    }
  }

  return (
    <div
      ref={tempRef}
      onBlur={manejarBlur}
      className='flex items-center p-1.5 hover:bg-accent hover:text-accent-foreground rounded-lg'
    >
      <input
        style={{ background: colorTemp }}
        className={`rounded-full size-4 shrink-0 cursor-pointer p-0 
        [&::-webkit-color-swatch-wrapper]:p-0
        [&::-webkit-color-swatch]:opacity-0 
        [&::-webkit-color-swatch]:border-none 
        [&::-webkit-color-swatch]:rounded-full
        [&::-moz-color-swatch]:border-none 
        [&::-moz-color-swatch]:rounded-full
        [&::-moz-color-swatch]:opacity-0
        `}
        type='color'
        value={colorTemp}
        onChange={e => setColorTemp(e.target.value)}
      />
      <Input
        autoFocus
        className='capitalize p-0 pl-2 border-none outline-none rounded-none h-[1.6rem] text-base'
        value={nombreTemp}
        onChange={e => setNombreTemp(e.target.value)}
        maxLength={50}
        onKeyDown={manejarEnter}
      />
    </div>
  )
}
