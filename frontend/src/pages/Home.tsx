import CalendarioHeader from '../components/CalendarioHeader'
import Details from '../components/Details'
import ListaActividades from '../components/ListaActividades'
import styles from './Home.module.css'

export default function Home() {
  return (
    <>
      <div className={styles.actividadesWrapper}>
        <ListaActividades />
      </div>
      <div className={styles.calendarioWrapper}>
        <CalendarioHeader />
      </div>
      <Details />
    </>
  )
}
