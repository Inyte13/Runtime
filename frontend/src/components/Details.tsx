import ListaBloques from './ListaBloques'
import styles from './Details.module.css'
import { useFechaStore } from '../store/fechaStore'
import { useEffect } from 'react'
import { useDiasStore } from '../store/diasStore'

export default function Details() {
  const fechaDetail = useFechaStore(state => state.getFechaDetail())
  const fechaISO = useFechaStore(state => state.getFechaISO())

  const fecha = useFechaStore(state => state.fecha)
  const diaDetail = useDiasStore(state => state.diaDetail)
  const bloques = diaDetail?.bloques || []

  const traerDiaDetail = useDiasStore(state => state.traerDiaDetail)
  const actualizarDia = useDiasStore(state => state.actualizarDia)
  
  useEffect(() => {
    traerDiaDetail()
  }, [fecha, traerDiaDetail])

  const manejarTitulo = async (e: React.FocusEvent<HTMLTextAreaElement>) => {
    await actualizarDia(fechaISO, { titulo: e.target.value })
  }
  return (
    <article className={styles.details}>
      <header className={styles.header}>
        <h2>{fechaDetail}</h2>
        <textarea
          defaultValue={diaDetail?.titulo || ''}
          placeholder='Añadir título'
          onBlur={manejarTitulo}
          maxLength={150}
        />
      </header>
      <ListaBloques bloques={bloques} />
    </article>
  )
}
