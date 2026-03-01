import { create } from 'zustand'
import {
  createActividad,
  readActividades,
  updateActividad,
} from '../services/actividadesServices'
import {
  ActividadCreate,
  ActividadRead,
  ActividadUpdate,
} from '../types/Actividad'
import { useColorStore } from './colorStore'

interface ActividadState {
  actividades: ActividadRead[]
  traerActividades: () => Promise<void>
  crearActividad: (actividad: ActividadCreate) => Promise<void>
  actualizarActividad: (id: number, actividad: ActividadUpdate) => Promise<void>
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
  actualizarActividad: async (id, actividad) => {
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
