import CalendarioHeader from '../components/CalendarioHeader'
import Details from '../components/Details'
import styles from './Home.module.css'
import { useState } from 'react'

export default function Home () {
  const [fecha, setFecha] = useState(new Date())
  const prevDia = () => {
    setFecha(d => new Date(d.getFullYear(), d.getMonth(), d.getDate() - 1))
  }
  const nextDia = () => {
    setFecha(d => new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1))
  }
  const irHoy = () => {
    setFecha(new Date())
  }
  return (
    <>
      <div className={styles.calendarioWrapper}>
        <CalendarioHeader
          fecha={fecha}
          prevDia={prevDia}
          nextDia={nextDia}
          irHoy={irHoy}
        />
      </div>
      <Details
        fecha={fecha}
      />
    </>
  )
}
