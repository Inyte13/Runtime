import ListaBloques from './ListaBloques'
import styles from './Details.module.css'
import { useFechaStore } from '../store/fechaStore'

export default function Details () {
  const fecha = useFechaStore(state => state.fecha)
  // Formateamos la fecha que tenemos de la store
  const date = fecha
    .toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'short'
    })
    .replace(/^./, c => c.toUpperCase())
  return (
    <article className={styles.details}>
      <header className={styles.header}>
        <h2>{date}</h2>
      </header>
      <ListaBloques />
    </article>
  )
}
