import { useEffect, useState } from 'react'
import CalendarioHeader from '../components/CalendarioHeader'
import Details from '../components/Details'
import styles from './Home.module.css'

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
  const [bloques, setBloques] = useState([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    async function fetchBloques () {
      try {
        setLoading(true)
        // Convierte la fecha a ISO (2026-01-07)
        const fechaISO = fecha.toISOString().split('T')[0]
        const response = await fetch(`http://127.0.0.1:8000/bloques/?fecha=${fechaISO}`)
        if (!response.ok) throw new Error('Error al cargar los bloques')
        const data = await response.json()
        setBloques(data)
      } catch (error) {
        console.error('Error fetching json:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchBloques()
  }, [fecha])
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
        bloques={bloques}
        loading={loading}
      />
    </>
  )
}
