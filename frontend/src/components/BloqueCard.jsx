import { useState } from 'react'
import styles from './BloqueCard.module.css'

export default function BloqueCard ({ bloque, manejarEliminacion }) {
  // Uppercase para el primer char
  const nombreBd = bloque.actividad.nombre
  const nombre = nombreBd.charAt(0).toUpperCase() + nombreBd.slice(1)

  const [color, setColor] = useState(bloque.actividad.color)
  const manejarCambioColor = async (e) => {
    const nuevoColor = e.target.value
    setColor(nuevoColor)
    await fetch(`/actividades/${bloque.actividad.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ color: nuevoColor })
    })
  }

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
      <header>
        <h2>
          <input
            type='color'
            value={color}
            className={styles.circulo}
            style={{ background: color }}
            // onChange solo para cambiar en el frontend
            onChange={e => setColor(e.target.value)}
            // onBlur se ejecuta cuando cambia el foco
            onBlur={manejarCambioColor}
          />
          {nombre}
          {bloque.duracion && (
            <span className={styles.duracion}>
              {bloque.duracion}h
            </span>
          )}
          <button
            className={styles.eliminarBtn}
            onClick={manejarEliminacion}
          >
            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-x'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M18 6l-12 12' /><path d='M6 6l12 12' /></svg>
          </button>
        </h2>
        <time dateTime={bloque.hora}>
          {bloque.hora} - {bloque.hora_fin}
        </time>
      </header>
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
