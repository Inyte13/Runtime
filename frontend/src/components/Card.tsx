import styles from './Card.module.css'
import CardHeader from './CardHeader'
import { useDiasStore } from '../store/diasStore'
import { useState } from 'react'
import { BloqueRead } from '../types/Bloque'

export default function Card({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const [color, setColor] = useState(bloque.actividad.color)
  const manejarDescripcion = async (e: React.FocusEvent<HTMLTextAreaElement>) => {
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  return (
    <article
      className={styles.bloque}
      style={{ '--color-bloque': color } as React.CSSProperties}
    >
      <CardHeader bloque={bloque} color={color} setColor={setColor} />
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
