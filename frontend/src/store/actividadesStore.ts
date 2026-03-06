import { create } from 'zustand'
import {
  createActividad,
  deleteActividad,
  readActividadesDetail,
  updateActividad,
} from '../services/actividadesServices'
import {
  ActividadCreate,
  ActividadReadDetail,
  ActividadUpdate,
} from '../types/Actividad'
import { useColorStore } from './colorStore'

interface ActividadState {
  actividades: ActividadRead[]
  traerActividades: () => Promise<void>
  crearActividad: (actividad: ActividadCreate) => Promise<void>
  actualizarActividad: (id: number, actividad: ActividadUpdate) => Promise<void>
  eliminarActividad: (id: number) => Promise<void>
}

export const useActividadesStore = create<ActividadState>(set => ({
  actividades: [],

  traerActividades: async () => {
    try {
      const data = await readActividades()
      set({ actividades: data })
      // Store Hydration: Para guardar los los colores para no repetirlos
      useColorStore.getState().setColores(data)
    } catch (err) {
      console.error('Error trayendo actividades:', err)
    }
  },

  crearActividad: async actividad => {
    try {
      const actividadNew = await createActividad(actividad)
      set(state => ({ actividades: [...state.actividades, actividadNew] }))
    } catch (err) {
      console.error('Error al crear la actividad', err)
    }
  },

  actualizarActividad: async (id, actividadNew) => {
    try {
      await updateActividad(id, actividadNew)
      set(state => ({
        actividades: state.actividades.map(actividad =>
          actividad.id === id ? { ...actividad, ...actividadNew } : actividad
        ),
      }))
    } catch (err) {
      console.error('Error actualizando la actividad', err)
    }
  },

  eliminarActividad: async id => {
    try {
      await deleteActividad(id)
      set(state => {
        if (!state.actividades) return state
        return {
          actividades: state.actividades.filter(
            actividad => actividad.id !== id
          ),
        }
      })
    } catch (err) {
      console.error('Error eliminando la actividad', err)
    }
  },
}))
