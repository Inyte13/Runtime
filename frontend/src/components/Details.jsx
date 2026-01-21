import ListaBloques from './ListaBloques'
import styles from './Details.module.css'
import { useFechaStore } from '../store/fechaStore'

function DetailHeader () {
  const { fecha } = useFechaStore()
  const date = fecha
    .toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'short'
    })
    .replace(/^./, c => c.toUpperCase())
  return (
    <header className={styles.header}>
      <h2>{date}</h2>
    </header>
  )
}

export default function Details () {
  return (
    <article className={styles.details}>
      <DetailHeader />
      <ListaBloques />
    </article>
  )
}
