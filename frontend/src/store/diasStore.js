import { create } from 'zustand'
import { useFechaStore } from './fechaStore'
import { readDiaDetail } from '../services/diasService'
import { createBloque, deleteBloque, updateBloque } from '../services/bloquesService'

export const useDiasStore = create((set, get) => ({
  dia: null,

  traerDia: async () => {
    const fechaISO = useFechaStore.getState().getFechaISO()
    try {
      const data = await readDiaDetail(fechaISO)
      set({ dia: data })
    } catch (err) {
      console.error('Error trayendo el dia', err)
      set({ dia: null })
    }
  },

  crearBloque: async () => {
    const fechaISO = useFechaStore.getState().getFechaISO()
    try {
      await createBloque({ fecha: fechaISO })
      await get().traerDia()
    } catch (err) {
      console.error('Error al crear el bloque', err)
    }
  },

  actualizarBloque: async (id, cambios) => {
    try {
      await updateBloque(id, cambios)
      await get().traerDia()
    } catch (err) {
      console.error('Error actualizando el bloque', err)
    }
  },

  eliminarBloque: async (id) => {
    try {
      await deleteBloque(id)
      await get().traerDia()
    } catch (err) {
      console.error('Error eliminando el bloque', err)
    }
  }
}))
