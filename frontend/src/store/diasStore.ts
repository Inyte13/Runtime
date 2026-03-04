import { readDiaDetail, sortDia, updateDia } from '../services/diasService'
import { create } from 'zustand'
import { useFechaStore } from './fechaStore'
import {
  createBloque,
  deleteBloque,
  updateBloque,
} from '../services/bloquesService'
import { DiaRead, DiaReadDetail, DiaUpdate } from '../types/Dia'
import { BloqueUpdate } from '../types/Bloque'
import { formatFechaISO } from '../utils/formatDate'
import { DragEndEvent } from '@dnd-kit/core'
import { modificarHora } from '../utils/hora'

interface DiasState {
  dia: DiaRead | null
  diaDetail: DiaReadDetail | null
  traerDiaDetail: () => Promise<void>
  actualizarDia: (fechaISO: string, dia: DiaUpdate) => Promise<void>
  crearBloque: () => Promise<void>
  actualizarBloque: (id: number, bloque: BloqueUpdate) => Promise<void>
  actualizarHoras: (id: number, duracion: number) => void
  reordenarBloques: (event: DragEndEvent) => Promise<void>
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
      const bloqueUpdate = await updateBloque(id, bloque)
      set(state => {
        if (!state.diaDetail) return state
        return {
          diaDetail: {
            // Conservamos título, estado y fecha
            ...state.diaDetail,
            bloques: state.diaDetail.bloques.map(bloque =>
              bloque.id === id ? { ...bloque, ...bloqueUpdate } : bloque
            ),
          },
        }
      })
    } catch (err) {
      console.error('Error actualizando el bloque', err)
    }
  },

  actualizarHoras: (id, duracion) => {
    set(state => {
      if (!state.diaDetail) return state
      const bloques = state.diaDetail.bloques

      // La posición del índice del bloque actualizado
      const indice = bloques.findIndex(bloque => bloque.id === id)
      if (indice === -1) return state

      const diferencia = duracion - (bloques[indice].duracion || 0)

      // Si la diferencia es la misma
      if (diferencia === 0) return state

      const newBloques = bloques.map((bloque, i) => {
        if (i === indice) {
          return {
            ...bloque,
            // Solo le cambiamos la duracion y la hora_fin la hora se queda como está
            duracion: duracion,
            hora_fin: modificarHora(bloque.hora, duracion),
          }
        }

        if (i > indice) {
          return {
            ...bloque,
            // Modificamos la hora y hora_fin
            hora: modificarHora(bloque.hora, diferencia),
            hora_fin: bloque.hora_fin
              ? modificarHora(bloque.hora_fin, diferencia)
              : bloque.hora_fin,
          }
        }
        return bloque
      })

      return {
        diaDetail: {
          ...state.diaDetail,
          bloques: newBloques,
        },
      }
    })
  },

  reordenarBloques: async event => {
    // active: lo que tienes agarrado
    // over: donde cayó
    const { active, over } = event

    if (
      !over || // Si lo soltó fuera de la lista
      active.id === over.id // Si lo soltó en el mismo lugar
    )
      return

    const diaDetail = useDiasStore.getState().diaDetail

    // Si por una casualidad no existe el diaDetail
    if (!diaDetail) return

    const bloques = [...diaDetail.bloques]
    const backup = [...bloques]

    const inicio = bloques.findIndex(bloque => bloque.id === active.id)
    const fin = bloques.findIndex(bloque => bloque.id === over.id)

    // Si por una casualidad los ids no existe
    if (inicio === -1 || fin === -1) return

    // Guardamos el value de la posicion inicio
    const [bloque] = bloques.splice(inicio, 1)
    // Insertamos nuestro bloque en la posicion final
    bloques.splice(fin, 0, bloque)

    // Buscamos el primer bloque sin duracion
    const bloqueSinDuracion = bloques.find(bloque => !bloque.duracion)
    if (
      bloqueSinDuracion && // Si existe:
      bloques.indexOf(bloqueSinDuracion) !== bloques.length - 1 // Y no es el ultimo
    )
      return

    set({
      diaDetail: {
        ...diaDetail,
        bloques: bloques,
      },
    })

    try {
      const ids = bloques.map(bloque => bloque.id)
      const fecha = useFechaStore.getState().fecha
      const fechaISO = formatFechaISO(fecha)
      const bloques_new = await sortDia(fechaISO, ids)
      set(state => {
        if (!state.diaDetail) return state
        return {
          diaDetail: {
            ...state.diaDetail,
            bloques: bloques_new,
          },
        }
      })
    } catch (error) {
      console.error('Error al reordenar los bloques:', error)
      // Rollback
      set({
        diaDetail: {
          ...diaDetail,
          bloques: backup,
        },
      })
    }
  },

  eliminarBloque: async id => {
    try {
      await deleteBloque(id)
      set(state => {
        if (!state.diaDetail) return state
        return {
          diaDetail: {
            ...state.diaDetail,
            bloques: state.diaDetail.bloques.filter(bloque => bloque.id !== id),
          },
        }
      })
    } catch (err) {
      console.error('Error eliminando el bloque', err)
    }
  },
}))
