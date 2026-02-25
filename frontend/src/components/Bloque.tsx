import { useDiasStore } from '../store/diasStore'
import { BloqueRead } from '../types/Bloque'
import { useColorStore } from '../store/colorStore'
import BloqueHeader from './BloqueHeader'
import { Input } from './ui/input'

export default function Bloque({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const color = useColorStore(
    state => state.colores[bloque.actividad.id] || bloque.actividad.color
  )
  const manejarDescripcion = async (e: React.FocusEvent<HTMLInputElement>) => {
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  return (
    <article
      className='border border-border border-l-2 rounded-md px-2 pb-2 pt-1 relative bg-card flex flex-col '
      style={{ borderLeftColor: `${color}95` }}
    >
      <BloqueHeader bloque={bloque} />
      <div>
        <span className='pl-1 text-foreground/70'>
          {bloque.hora} - {bloque.hora_fin}
        </span>
      </div>
      <Input
        style={{ '--color': `${color}` } as React.CSSProperties}
        className='border-0 border-b border-transparent focus:border-(--color) outline-none rounded-none italic h-[1.6rem] text-base pr-0 pl-1 mt-1' 
        defaultValue={bloque.descripcion || ''}
        placeholder='Añadir descripción'
        onBlur={manejarDescripcion}
        maxLength={255}
      />
    </article>
  )
}
