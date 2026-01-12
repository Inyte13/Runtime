import { useState } from 'react'
import styles from './Card.module.css'
import CardHeader from './CardHeader'

export default function Card ({ bloque, manejarEliminacion }) {
  const [color, setColor] = useState(bloque.actividad.color)
  const [description, setDescription] = useState(bloque.descripcion || '')

  const manejarDescripcion = async () => {
    await fetch(`/bloques/${bloque.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ descripcion: description })
    })
  }

  return (
    <article
      className={styles.bloque}
      style={{ '--color-bloque': color }}
    >
      <CardHeader
        bloque={bloque}
        color={color}
        setColor={setColor}
        manejarEliminacion={manejarEliminacion}
      />
      <div>
        <button className={styles.timeBtn}>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-clock-edit'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M21 12a9 9 0 1 0 -9.972 8.948c.32 .034 .644 .052 .972 .052' /><path d='M12 7v5l2 2' /><path d='M18.42 15.61a2.1 2.1 0 0 1 2.97 2.97l-3.39 3.42h-3v-3l3.42 -3.39' /></svg>
        </button>
        <time dateTime={bloque.hora}>
          {bloque.hora} - {bloque.hora_fin}
        </time>
      </div>
      <textarea
        className={styles.descripcion}
        value={description}
        placeholder='Añadir descripción'
        onChange={e => setDescription(e.target.value)}
        onBlur={manejarDescripcion}
        maxLength={255}
      />
    </article>
  )
}
