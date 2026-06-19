import { create } from 'zustand'
import {
  createActividad,
  deleteActividad,
  readActividadesDetail,
  updateActividad,
} from '../services/actividadServices'
import {
  ActividadCreate,
  ActividadReadDetail,
  ActividadUpdate,
} from '../types/Actividad'
import { useColorStore } from './colorStore'

interface ActividadState {
  actividadesDetail: ActividadReadDetail[]
  traerActividadesDetail: () => Promise<void>
  crearActividad: (actividad: ActividadCreate) => Promise<void>
  actualizarActividad: (id: number, actividad: ActividadUpdate) => Promise<void>
  eliminarActividad: (id: number) => Promise<void>
}

export const useActividadesStore = create<ActividadState>(set => ({
  actividadesDetail: [],

  traerActividadesDetail: async () => {
    try {
      const data = await readActividadesDetail()
      set({ actividadesDetail: data })
      // Store Hydration: Para guardar los los colores para no repetirlos
      useColorStore.getState().setColores(data)
    } catch (err) {
      console.error('Error trayendo actividades:', err)
    }
  },

  crearActividad: async actividadNew => {
    try {
      const actividad = await createActividad(actividadNew)
      set(state => ({
        actividadesDetail: [...state.actividadesDetail, actividad],
      }))
    } catch (err) {
      console.error('Error al crear la actividad', err)
    }
  },

  actualizarActividad: async (id, actividadNew) => {
    try {
      const actividad = await updateActividad(id, actividadNew)

      // Si solo cambiaste color no hagas nada mas
      if (Object.keys(actividadNew).every(k => k === 'color')) return
      
      set(state => ({
        actividadesDetail: state.actividadesDetail.map(actividadDetail =>
          actividadDetail.id === id
            ? { ...actividadDetail, ...actividad }
            : actividadDetail
        ),
      }))
    } catch (err) {
      console.error('Error actualizando la actividad', err)
    }
  },

  eliminarActividad: async id => {
    try {
      await deleteActividad(id)
      set(state => ({
        actividadesDetail: state.actividadesDetail.filter(
          actividad => actividad.id !== id
        ),
      }))
    } catch (err) {
      console.error('Error eliminando la actividad', err)
    }
  },
}))
