import ListaBloques from './ListaBloques'
import styles from './Details.module.css'
import { useFechaStore } from '../store/fechaStore.ts'

export default function Details () {
  const FechaDetail = useFechaStore(state => state.getFechaDetail())
  return (
    <article className={styles.details}>
      <header className={styles.header}>
        <h2>{FechaDetail}</h2>
      </header>
      <ListaBloques />
    </article>
  )
}
