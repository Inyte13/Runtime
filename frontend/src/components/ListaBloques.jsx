import { useEffect } from 'react'
import { useBloquesStore } from '../store/bloquesStore.js'
import { useFechaStore } from '../store/fechaStore.js'
import Card from './Card.jsx'
import styles from './ListaBloques.module.css'

export default function ListaBloques () {
  const { bloques, loading, crearBloque, traerBloques } = useBloquesStore()
  const { fecha } = useFechaStore()
  useEffect(() => {
    traerBloques()
  }, [fecha])

  return (
    <>
      <div className={styles.listaBloques}>
        {loading && <p>Cargando...</p>}
        {!loading && bloques.length === 0 && <p>Este día no tiene ningún bloque</p>}
        {bloques.map(bloque => (
          <Card
            key={bloque.id}
            bloque={bloque}
          />
        ))}
        <button className='btn' onClick={crearBloque}>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-plus'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M12 5l0 14' /><path d='M5 12l14 0' /></svg>
        </button>
      </div>
    </>
  )
}
