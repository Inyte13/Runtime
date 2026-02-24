import Calendario from '../components/Calendario'
import Dia from '../components/Dia'
import ListaActividades from '../components/ListaActividades'

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
