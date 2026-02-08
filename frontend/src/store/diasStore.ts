import { create } from 'zustand'
import { useFechaStore } from './fechaStore'
import { readDiaDetail } from '../services/diasService'
import { createBloque, deleteBloque, updateBloque } from '../services/bloquesService'
import { DiaReadDetail } from '../types/Dia'
import { BloqueUpdate } from '../types/Bloque'

interface DiasState {
  dia: DiaReadDetail | null
  traerDia: () => Promise<void>
  crearBloque: () => Promise<void>
  actualizarBloque: (id: number, bloque: BloqueUpdate) => Promise<void>
  eliminarBloque: (id: number) => Promise<void>
}

export const useDiasStore = create<DiasState>((set, get) => ({
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

  actualizarBloque: async (id, bloque) => {
    try {
      await updateBloque(id, bloque)
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
