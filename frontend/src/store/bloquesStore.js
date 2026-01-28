import { create } from 'zustand'
import { createBloque, deleteBloque, readBloques, updateBloque } from '../services/bloquesService'
import { useFechaStore } from './fechaStore'

export const useBloquesStore = create((set, get) => ({
  bloques: [],

  traerBloques: async () => {
    const { fecha } = useFechaStore.getState()
    try {
      const data = await readBloques(fecha)
      set({ bloques: data })
    } catch (err) {
      console.error('Error trayendo bloques:', err)
    }
  },

  crearBloque: async () => {
    const { bloques } = get()
    const { fecha } = useFechaStore.getState()
    try {
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
    }
  },

  actualizarBloque: async (id, cambios) => {
    try {
      await updateBloque(id, cambios)
      await get().traerBloques()
    } catch (err) {
      console.error('Error actualizando el bloque', err)
    }
  },

  eliminarBloque: async (id) => {
    try {
      await deleteBloque(id)
      await get().traerBloques()
    } catch (err) {
      console.error('Error eliminando el bloque', err)
    }
  }
}))
