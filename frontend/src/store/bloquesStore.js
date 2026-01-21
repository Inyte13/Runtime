import { create } from 'zustand'
import { createBloque, deleteBloque, readBloques, updateBloque } from '../services/bloquesService'
import { useFechaStore } from './fechaStore'

export const useBloquesStore = create((set, get) => ({
  bloques: [],
  loading: false,

  traerBloques: async () => {
    const { fecha } = useFechaStore.getState()
    try {
      set({ loading: true })
      const data = await readBloques(fecha)
      set({ bloques: data })
    } catch (err) {
      console.error('Error trayendo bloques:', err)
    } finally {
      set({ loading: false })
    }
  },

  crearBloque: async () => {
    const { bloques } = get()
    const { fecha } = useFechaStore.getState()
    try {
      set({ loading: true })
      let bloque
      if (bloques.length === 0) {
        bloque = {
          id_actividad: 1,
          descripcion: '',
          fecha: fecha.toLocaleDateString('sv-SE'),
          hora: '00:00'
        }
      } else {
        const anterior = bloques[bloques.length - 1]
        bloque = {
          id_actividad: 2,
          descripcion: '',
          fecha: fecha.toLocaleDateString('sv-SE'),
          hora: anterior.hora_fin
        }
      }
      await createBloque(bloque)
      await get().traerBloques()
    } catch (err) {
      console.error('Error al crear el bloque', err)
    } finally {
      set({ loading: false })
    }
  },

  actualizarBloque: async (id, cambios) => {
    try {
      set({ loading: true })
      await updateBloque(id, cambios)
      await get().traerBloques()
    } catch (err) {
      console.error('Error actualizando el bloque', err)
    } finally {
      set({ loading: false })
    }
  },

  eliminarBloque: async (id) => {
    try {
      set({ loading: true })
      await deleteBloque(id)
      await get().traerBloques()
    } catch (err) {
      console.error('Error eliminando el bloque', err)
    } finally {
      set({ loading: false })
    }
  }
}))
