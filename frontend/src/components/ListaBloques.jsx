import useBloques from '../hooks/useBloques'
import Card from './Card.jsx'
import styles from './ListaBloques.module.css'

export default function ListaBloques ({ fecha }) {
  const { bloques, loading, fetchBloques, eliminarBloque } = useBloques(fecha)
  const manejarAnadir = async () => {
    let nuevoBloque

    if (bloques.length === 0) {
      nuevoBloque = {
        id_actividad: 1,
        descripcion: '',
        fecha: fecha.toLocaleDateString('sv-SE'),
        hora: '00:00'
      }
    } else {
      const anterior = bloques[bloques.length - 1]
      nuevoBloque = {
        id_actividad: 2,
        descripcion: '',
        fecha: fecha.toLocaleDateString('sv-SE'),
        hora: anterior.hora_fin
      }
    }
    const response = await fetch('/bloques', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevoBloque)
    })
    if (response.ok) {
      fetchBloques()
    }
  }

  return (
    <>
      <div className={styles.listaBloques}>
        {loading && (
          <p>Cargando...</p>
        )}
        {bloques.length === 0 && (
          <p>Este día no tiene ningún bloque</p>
        )}
        {bloques.map(bloque => (
          <Card
            key={bloque.id}
            bloque={bloque}
            manejarEliminacion={() => eliminarBloque(bloque.id)}
          />
        ))}
        <button className='btn' onClick={manejarAnadir}>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-plus'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M12 5l0 14' /><path d='M5 12l14 0' /></svg>
        </button>
      </div>
    </>
  )
}
