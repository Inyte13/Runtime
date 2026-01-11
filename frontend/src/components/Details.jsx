import ListaBloques from './ListaBloques'
import styles from './Details.module.css'

function DetailHeader ({ date }) {
  const fecha = date
    .toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'short'
    })
    .replace(/^./, c => c.toUpperCase())
  return (
    <header className={styles.header}>
      <h2>{fecha}</h2>
    </header>
  )
}

export default function Details ({ fecha }) {
  return (
    <article>
      <DetailHeader date={fecha} />
      <ListaBloques
        fecha={fecha}
      />
    </article>
  )
}
