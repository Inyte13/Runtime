import { useEffect } from 'react'
import { useActividadesStore } from '../store/actividadesStore'
import Actividad from './Actividad'
import styles from './ListaActividades.module.css'

export default function ListaActividades() {
  const actividades = useActividadesStore(state => state.actividades)
  const traerActividades = useActividadesStore(state => state.traerActividades)
  useEffect(() => {
    traerActividades()
  }, [traerActividades])

  const crearActividad = useActividadesStore(state => state.crearActividad)
  return (
    <div className={styles.listaActividades}>
      {actividades.map(actividad => (
        <Actividad key={actividad.id} actividad={actividad} />
      ))}
      <button className='btn' onClick={crearActividad}>
        <svg
          xmlns='http://www.w3.org/2000/svg'
          width='24'
          height='24'
          viewBox='0 0 24 24'
          fill='none'
          stroke='currentColor'
          strokeWidth='2'
          strokeLinecap='round'
          strokeLinejoin='round'
          className='icon icon-tabler icons-tabler-outline icon-tabler-plus'
        >
          <path stroke='none' d='M0 0h24v24H0z' fill='none' />
          <path d='M12 5l0 14' />
          <path d='M5 12l14 0' />
        </svg>
      </button>
    </div>
  )
}
