import { create } from 'zustand'
import { readActividades, updateActividad } from '../services/actividadesServices'
import { ActividadRead, ActividadUpdate } from '../types/Actividad'

interface ActividadState {
  actividades: ActividadRead[]
  traerActividades: () => Promise<void>
  actualizarActividad: (id: number, actividad: ActividadUpdate) => Promise<void>
}

export const useActividadesStore = create<ActividadState>((set) => ({
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
