import CalendarioHeader from '../components/CalendarioHeader'
import Details from '../components/Details'
import styles from './Home.module.css'

export default function Home () {
  return (
    <>
      <div className={styles.calendarioWrapper}>
        <CalendarioHeader />
      </div>
      <Details />
    </>
  )
}
