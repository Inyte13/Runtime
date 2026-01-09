import styles from './BloqueCard.module.css'
export default function BloqueCard ({ bloque }) {
  return (
    <article className={styles.bloque}>
      <header>
        <h2><span />{bloque.actividad.nombre}</h2>
        <time dateTime={bloque.hora}>
          {bloque.hora} - 11:00
        </time>
        <span>{}</span>
      </header>
      {
        bloque.descripcion
          ? <p>{bloque.descripcion}</p>
          : <button>Añadir descripción</button>
      }
    </article>
  )
}
