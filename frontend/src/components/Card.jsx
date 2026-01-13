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

  const [hora, setHora] = useState(bloque.hora || '')
  const [horaFin, setHoraFin] = useState(bloque.hora_fin || '')
  const manejarHora = async () => {
    const response = await fetch(`/bloques/${bloque.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hora })
    })
    if (response.ok) {
      const updated = await response.json()
      setHora(updated.hora)
      setHoraFin(updated.hora_fin)
      bloque.hora = updated.hora
      bloque.hora_fin = updated.hora_fin
    }
  }
  const actualizarDatosBloque = (updated) => {
    setHoraFin(updated.hora_fin)
    bloque.duracion = updated.duracion
    bloque.hora_fin = updated.hora_fin
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
        actualizarDatosBloque={actualizarDatosBloque}
      />
      <div>
        <input
          type='time'
          value={hora}
          onChange={e => setHora(e.target.value)}
          onBlur={manejarHora}
          step='1800'
        />
        <span> - {horaFin}</span>
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
