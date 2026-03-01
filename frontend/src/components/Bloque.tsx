import { useDiasStore } from '../store/diasStore'
import { BloqueRead } from '../types/Bloque'
import BloqueHeader from './BloqueHeader'
import { Input } from './ui/input'
import { memo } from 'react'
import useDuracionBloque from '../hooks/useDuracionBloque'
import BloqueColor from './BloqueColor'

export default memo(function Bloque({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const descripcion = bloque.descripcion || ''
  const manejarDescripcion = async (e: React.FocusEvent<HTMLInputElement>) => {
    const newDescripcion = e.target.value
    if (newDescripcion === descripcion) return
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  const { duracionLocal, manejarDuracion, horaFin } = useDuracionBloque(
    bloque.id,
    bloque.duracion,
    bloque.hora
  )

  return (
    <BloqueColor
      id={bloque.actividad.id}
      colorDefault={bloque.actividad.color}
      className='border border-border border-l-2 rounded-md px-2 pb-2 pt-1 relative bg-card flex flex-col'
    >
      <BloqueHeader
        bloque={bloque}
        duracion={duracionLocal}
        manejarDuracion={manejarDuracion}
      />
      <div>
        <span className='pl-1 text-foreground/70'>
          {bloque.hora} {horaFin && `- ${horaFin}`}
        </span>
      </div>
      <Input
        className='border-0 border-b border-transparent focus:border-(--color) outline-none rounded-none italic h-[1.6rem] text-base pr-0 pl-1 mt-1'
        defaultValue={descripcion}
        placeholder='Añadir descripción'
        onBlur={manejarDescripcion}
        maxLength={255}
      />
    </BloqueColor>
  )
})
