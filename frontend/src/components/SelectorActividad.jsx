import { useEffect, useRef, useState } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import { useBloquesStore } from '../store/bloquesStore'
import './SelectorActividad.module.css'

export default function SelectorActividad ({ bloque, setColor }) {
  const { actualizarBloque } = useBloquesStore()
  const { actividades, traerActividades } = useActividadesStore()
  const [selector, setSelector] = useState(false)
  const modalRef = useRef(null)

  useEffect(() => {
    const manejarClickOut = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        setSelector(false)
      }
    }
    document.addEventListener('mousedown', manejarClickOut)
    return () => document.removeEventListener('mousedown', manejarClickOut)
  }, [])

  const manejarSelector = async (actividad) => {
    await actualizarBloque(bloque.id, { id_actividad: actividad.id })
    setColor(actividad.color)
  }

  const manejarClick = () => {
    setSelector(!selector)
    !selector && traerActividades()
  }

  return (
    <div ref={modalRef}>
      <button onClick={manejarClick}>
        <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-menu-2'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M4 6l16 0' /><path d='M4 12l16 0' /><path d='M4 18l16 0' /></svg>
        {selector && (
          <div>
            <ul>
              {actividades.map(act => (
                <li key={act.id} onClick={() => manejarSelector(act)}>
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
    </div>
  )
}
