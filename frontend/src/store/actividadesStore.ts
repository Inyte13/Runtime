import { create } from 'zustand'
import {
  createActividad,
  readActividades,
  updateActividad,
} from '../services/actividadesServices'
import { ActividadCreate, ActividadRead, ActividadUpdate } from '../types/Actividad'

interface ActividadState {
  actividades: ActividadRead[]
  crearActividad: (actividad: ActividadCreate) => Promise<void>
  traerActividades: () => Promise<void>
  actualizarActividad: (id: number, actividad: ActividadUpdate) => Promise<void>
}

export const useActividadesStore = create<ActividadState>((set, get) => ({
  actividades: [],
  crearActividad: async (actividad) => {
    try {
      await createActividad(actividad)
      await get().traerActividades()
    } catch (err) {
      console.error('Error al crear la actividad', err)
    }
  },

  traerActividades: async () => {
    try {
      const data = await readActividades()
      set({ actividades: data })
      // sincronizar colores en el store global
      // useColorStore.setState({
      //   colores: Object.fromEntries(data.map(a => [a.id, a.color])),
      // })
    } catch (err) {
      console.error('Error trayendo actividades:', err)
    }
  },
  actualizarActividad: async (id, actividad) => {
    try {
      await updateActividad(id, actividad)
      await get().traerActividades()
      // sincronizar colores en el store global
      // useColorStore.setState({
      //   colores: Object.fromEntries(data.map(a => [a.id, a.color])),
      // })
    } catch (err) {
      console.error('Error actualizando la actividad', err)
    }
  },
}))
