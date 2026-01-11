import { useEffect, useState } from 'react'

export default function useBloques (fecha) {
  const [bloques, setBloques] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchBloques = async () => {
    try {
      setLoading(true)
      // Convierte la fecha a ISO (2026-01-07)
      const fechaISO = fecha.toLocaleDateString('sv-SE') // Hora local
      const response = await fetch(`/bloques/?fecha=${fechaISO}`)
      if (!response.ok) throw new Error('Error al cargar los bloques')
      const data = await response.json()
      setBloques(data)
    } catch (error) {
      console.error('Error fetching json:', error)
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => {
    fetchBloques()
  }, [fecha])

  const eliminarBloque = async (id) => {
    try {
      const response = await fetch(`/bloques/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw Error('Error al eliminar el bloque')
      setBloques(prev => prev.filter(b => b.id !== id))
    } catch (error) {
      console.error('Error eliminando bloque:', error)
    }
  }
  return { bloques, setBloques, loading, fetchBloques, eliminarBloque }
}
