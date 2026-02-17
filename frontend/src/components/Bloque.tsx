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
  const manejarDescripcion = async (
    e: React.FocusEvent<HTMLInputElement>
  ) => {
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  return (
    <article
      style={{ '--color-bloque': color } as React.CSSProperties}
    >
      <BloqueHeader bloque={bloque} />
      <div>
        <span>
          {bloque.hora} - {bloque.hora_fin}
        </span>
      </div>
      <Input
        defaultValue={bloque?.descripcion || ''}
        placeholder='Añadir descripción'
        onBlur={manejarDescripcion}
        maxLength={255}
      />
    </article>
  )
}
