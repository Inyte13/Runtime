import styles from './Card.module.css'
import CardHeader from './CardHeader'
import { useDiasStore } from '../store/diasStore'
import { BloqueRead } from '../types/Bloque'
import { useColorStore } from '../store/colorStore'

export default function Card({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const color = useColorStore(
    state => state.colores[bloque.actividad.id] || bloque.actividad.color
  )
  const manejarDescripcion = async (
    e: React.FocusEvent<HTMLTextAreaElement>
  ) => {
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  return (
    <article
      className={styles.bloque}
      style={{ '--color-bloque': color } as React.CSSProperties}
    >
      <CardHeader bloque={bloque} />
      <div>
        <span>
          {bloque.hora} - {bloque.hora_fin}
        </span>
      </div>
      <textarea
        defaultValue={bloque.descripcion || ''}
        placeholder='Añadir descripción'
        onBlur={manejarDescripcion}
        maxLength={255}
      />
    </article>
  )
}
