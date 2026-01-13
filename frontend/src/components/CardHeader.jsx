import { useEffect, useRef, useState } from 'react'
import styles from './CardHeader.module.css'

export default function CardHeader ({ bloque, setColor, color, manejarEliminacion, actualizarDatosBloque }) {
  // Uppercase para el primer char
  const nombreBd = bloque.actividad.nombre
  const nombre = nombreBd.charAt(0).toUpperCase() + nombreBd.slice(1)

  const [selector, setSelector] = useState(false)
  const [actividades, setActividades] = useState([])
  const fetchActividades = async () => {
    try {
      const response = await fetch('/actividades')
      if (!response.ok) throw new Error('Error al cargar las actividades')
      const data = await response.json()
      setActividades(data)
    } catch (error) {
      console.error('Error fetching json:', error)
    }
  }

  const manejarSeleccionActividad = async (actividad) => {
    try {
      await fetch(`/bloques/${bloque.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_actividad: actividad.id })
      })
      bloque.actividad = actividad
      setColor(actividad.color)
      setSelector(false)
    } catch (error) {
      console.error(error)
    }
  }

  const manejarClick = () => {
    setSelector(prev => !prev)
    !selector && fetchActividades()
  }

  const modalRef = useRef(null)
  useEffect(() => {
    const manejarClickOut = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        setSelector(false)
      }
    }
    document.addEventListener('mousedown', manejarClickOut)
    return () => {
      document.removeEventListener('mousedown', manejarClickOut)
    }
  }, [])

  const manejarCambioColor = async (e) => {
    const nuevoColor = e.target.value
    setColor(nuevoColor)
    await fetch(`/actividades/${bloque.actividad.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ color: nuevoColor })
    })
  }

  const [duracion, setDuracion] = useState(bloque.duracion || 0)
  const manejarDuracion = async (newDuracion) => {
    const response = await fetch(`/bloques/${bloque.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ duracion: newDuracion })
    })
    if (response.ok) {
      const updated = await response.json()
      setDuracion(updated.duracion)
      actualizarDatosBloque(updated)
    }
  }
  const nextTime = () => {
    const newDuracion = parseFloat(duracion) + 0.5
    setDuracion(newDuracion)
    manejarDuracion(newDuracion)
  }
  const prevTime = () => {
    const newDuracion = Math.max(0, parseFloat(duracion) - 0.5)
    setDuracion(newDuracion)
    manejarDuracion(newDuracion)
  }
  return (
    <header>
      <h2 className={styles.h2} ref={modalRef}>
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
        <button
          className={styles.editarBtn}
          onClick={manejarClick}
        >
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-menu-2'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M4 6l16 0' /><path d='M4 12l16 0' /><path d='M4 18l16 0' /></svg>
          {selector && (
            <div className={styles.modal}>
              <ul>
                {actividades.map(act => (
                  <li key={act.id} onClick={() => manejarSeleccionActividad(act)}>
                    <span style={{ background: act.color }} />
                    <a>
                      {act.nombre.charAt(0).toUpperCase() + act.nombre.slice(1)}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </button>

        <div className={styles.duracion}>
          <input
            type='number'
            value={duracion}
            readOnly
          />
          <span>h</span>
          <div className={styles.stepper}>
            <button onClick={prevTime}>
              <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-up'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M6 15l6 -6l6 6' /></svg>
            </button>
            <button onClick={nextTime}>
              <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-down'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M6 9l6 6l6 -6' /></svg>
            </button>
          </div>
        </div>

        <button
          className={styles.eliminarBtn}
          onClick={manejarEliminacion}
        >
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-x'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M18 6l-12 12' /><path d='M6 6l12 12' /></svg>
        </button>

      </h2>
    </header>
  )
}
