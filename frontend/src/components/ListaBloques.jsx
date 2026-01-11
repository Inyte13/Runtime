import useBloques from '../hooks/useBloques'
import BloqueCard from './BloqueCard'
import styles from './ListaBloques.module.css'

export default function ListaBloques ({ fecha }) {
  const { bloques, loading, fetchBloques, eliminarBloque } = useBloques(fecha)
  const manejarAnadir = async () => {
    const nuevoBloque = {
      id_actividad: 13,
      descripcion: '',
      fecha: fecha.toLocaleDateString('sv-SE'),
      hora: '23:30'
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
          <BloqueCard
            key={bloque.id}
            bloque={bloque}
            manejarEliminacion={() => eliminarBloque(bloque.id)}
          />
        ))}
        <button className='btn' onClick={manejarAnadir}>Añadir</button>
      </div>
    </>
  )
}
