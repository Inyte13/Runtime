import styles from './CardHeader.module.css'
import { useBloquesStore } from '../store/bloquesStore'
import ColorPicker from './ColorPicker'
import SelectorActividad from './SelectorActividad'
import { useState } from 'react'

export default function CardHeader ({ bloque, color, setColor }) {
  const actualizarBloque = useBloquesStore(state => state.actualizarBloque)
  const eliminarBloque = useBloquesStore(state => state.eliminarBloque)
  const [duracion, setDuracion] = useState(bloque.duracion || 0)

  // Uppercase para el primer char
  const nombreBd = bloque.actividad.nombre
  const nombre = nombreBd.charAt(0).toUpperCase() + nombreBd.slice(1)

  const manejarDuracion = async (newDuracion) => {
    setDuracion(newDuracion)
    await actualizarBloque(bloque.id, { duracion: newDuracion })
  }
  const nextTime = () => {
    const newDuracion = parseFloat(duracion) + 0.5
    manejarDuracion(newDuracion)
  }
  const prevTime = () => {
    const newDuracion = Math.max(0, parseFloat(duracion) - 0.5)
    manejarDuracion(newDuracion)
  }
  return (
    <header>
      <h2 className={styles.h2}>
        <ColorPicker
          bloque={bloque}
          color={color}
          setColor={setColor}
        />
        {nombre}
        <SelectorActividad
          bloque={bloque}
          setColor={setColor}
        />
        <div className={styles.duracion}>
          <span>{duracion || '0'}h</span>
          <div className={styles.stepper}>
            <button
              onClick={prevTime}
              disabled={duracion === 0}
              className={
                `${styles.stepBtn} ${duracion === 0 ? styles.disabledBtn : ''}`
              }
            >
              <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-up'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M6 15l6 -6l6 6' /></svg>
            </button>
            <button onClick={nextTime}>
              <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-down'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M6 9l6 6l6 -6' /></svg>
            </button>
          </div>
        </div>

        <button
          className={styles.eliminarBtn}
          onClick={() => eliminarBloque(bloque.id)}
        >
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-x'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M18 6l-12 12' /><path d='M6 6l12 12' /></svg>
        </button>

      </h2>
    </header>
  )
}
