import { create } from 'zustand'
import { readActividades, updateActividad } from '../services/actividadesServices'

export const useActividadesStore = create((set, get) => ({
  actividades: [],
  loading: false,
  traerActividades: async () => {
    try {
      set({ loading: true })
      const data = await readActividades()
      set({ actividades: data })
    } catch (err) {
      console.error('Error trayendo actividades:', err)
    } finally {
      set({ loading: false })
    }
  },
  actualizarActividad: async (id, cambios) => {
    try {
      set({ loading: true })
      await updateActividad(id, cambios)
    } catch (err) {
      console.error('Error actualizando la actividad')
    } finally {
      set({ loading: false })
    }
  }
}))
