import { create } from 'zustand'
import { useFechaStore } from './fechaStore'
import { readDiaDetail, updateDia } from '../services/diasService'
import {
  createBloque,
  deleteBloque,
  updateBloque,
} from '../services/bloquesService'
import { DiaRead, DiaReadDetail, DiaUpdate } from '../types/Dia'
import { BloqueUpdate } from '../types/Bloque'
import { formatFechaISO } from '../utils/formatDate'

interface DiasState {
  dia: DiaRead | null
  diaDetail: DiaReadDetail | null
  traerDia: () => Promise<void>
  traerDiaDetail: () => Promise<void>
  actualizarDia: (fechaISO: string, dia: DiaUpdate) => Promise<void>
  crearBloque: () => Promise<void>
  actualizarBloque: (id: number, bloque: BloqueUpdate) => Promise<void>
  eliminarBloque: (id: number) => Promise<void>
}

export const useDiasStore = create<DiasState>(set => ({
  dia: null,
  diaDetail: null,

  traerDia: async () => {
    const fecha = useFechaStore.getState().fecha
    const fechaISO = formatFechaISO(fecha)
    try {
      const data = await readDia(fechaISO)
      set({ dia: data })
    } catch (err) {
      console.error('Error trayendo el dia', err)
      set({ dia: null })
    }
  },

  traerDiaDetail: async () => {
    const fecha = useFechaStore.getState().fecha
    const fechaISO = formatFechaISO(fecha)
    try {
      const data = await readDiaDetail(fechaISO)
      set({ diaDetail: data })
    } catch (err) {
      console.error('Error trayendo el dia detail', err)
      set({ diaDetail: null })
    }
  },

  actualizarDia: async (fechaISO, dia) => {
    try {
      await updateDia(fechaISO, dia)
      await get().traerDia()
    } catch (err) {
      console.error('Error actualizando el dia', err)
    }
  },

  crearBloque: async () => {
    const fecha = useFechaStore.getState().fecha
    const fechaISO = formatFechaISO(fecha)
    try {
      await createBloque({ fecha: fechaISO })
      await get().traerDiaDetail()
    } catch (err) {
      console.error('Error al crear el bloque', err)
    }
  },

  actualizarBloque: async (id, bloque) => {
    try {
      await updateBloque(id, bloque)
      await get().traerDiaDetail()
    } catch (err) {
      console.error('Error actualizando el bloque', err)
    }
  },

  eliminarBloque: async id => {
    try {
      await deleteBloque(id)
      await get().traerDiaDetail()
    } catch (err) {
      console.error('Error eliminando el bloque', err)
    }
  },
}))
