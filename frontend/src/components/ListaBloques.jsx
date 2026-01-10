import BloqueCard from './BloqueCard'
import styles from './ListaBloques.module.css'

export default function ListaBloques ({ bloques, loading }) {
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
          <BloqueCard key={bloque.id} bloque={bloque} />
        ))}
        <button className='btn'>Añadir</button>
      </div>
    </>
  )
}
