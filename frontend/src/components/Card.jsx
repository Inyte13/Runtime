import styles from './Card.module.css'
import CardHeader from './CardHeader'
import { useDiasStore } from '../store/diasStore.ts'
import { useState } from 'react'

export default function Card({ bloque }) {
  const actualizarBloque = useDiasStore((state) => state.actualizarBloque)
  const [color, setColor] = useState(bloque.actividad.color)
  const manejarDescripcion = async (e) => {
    await actualizarBloque(bloque.id, { descripcion: e.target.value })
  }

  return (
    <article className={styles.bloque} style={{ '--color-bloque': color }}>
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
