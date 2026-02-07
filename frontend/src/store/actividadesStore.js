import { create } from 'zustand'
import { readActividades, updateActividad } from '../services/actividadesServices'

export const useActividadesStore = create((set) => ({
  actividades: [],
  traerActividades: async () => {
    try {
      const data = await readActividades()
      set({ actividades: data })
    } catch (err) {
      console.error('Error trayendo actividades:', err)
    }
  },
  actualizarActividad: async (id, cambios) => {
    try {
      await updateActividad(id, cambios)
    } catch (err) {
      console.error('Error actualizando la actividad', err)
    }
  }
}))
