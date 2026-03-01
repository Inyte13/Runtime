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
  traerDiaDetail: () => Promise<void>
  actualizarDia: (fechaISO: string, dia: DiaUpdate) => Promise<void>
  crearBloque: () => Promise<void>
  actualizarBloque: (id: number, bloque: BloqueUpdate) => Promise<void>
  eliminarBloque: (id: number) => Promise<void>
}

export const useDiasStore = create<DiasState>(set => ({
  dia: null,
  diaDetail: null,

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
      const newDia = await updateDia(fechaISO, dia)
      set(state => ({
        // Reemplazamos todo (título, estado y fecha) porque son pocas props (mejor)
        dia: newDia,
        // Al diaDetail le cambiamos solo los valores de dia
        diaDetail: state.diaDetail ? { ...state.diaDetail, ...newDia } : null,
      }))
    } catch (err) {
      console.error('Error actualizando el dia', err)
    }
  },

  crearBloque: async () => {
    const fecha = useFechaStore.getState().fecha
    const fechaISO = formatFechaISO(fecha)
    try {
      const bloque = await createBloque({ fecha: fechaISO })
      set(state => {
        if (state.diaDetail) {
          return {
            diaDetail: {
              // Conservamos título, estado y fecha
              ...state.diaDetail,
              // Hacemos una copia en una dirección diferente de memoria
              // Los elementos copiados mantienen su misma referencia de memoria
              bloques: [...state.diaDetail.bloques, bloque],
            },
          }
        }
        // Si no hay diaDetail crearmos uno falso confiando en que el backend lo creo para ser rapido
        return {
          diaDetail: {
            fecha: fechaISO,
            estado: 2,
            bloques: [bloque],
          },
        }
      })
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
