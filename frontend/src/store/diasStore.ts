import {
  readDiaDetail,
  readDiasResumen,
  sortDia,
  updateDia,
} from '../services/dia-service'
import { create } from 'zustand'
import { useFechaStore } from './fechaStore'
import {
  createBloque,
  deleteBloque,
  updateBloque,
} from '../services/bloque-service'
import { DiaReadDetail, DiaResumen, DiaUpdate } from '../types/dia'
import { BloqueUpdate } from '../types/bloque'
import { formatFechaISO } from '../utils/formatDate'
import { DragEndEvent } from '@dnd-kit/core'
import { modificarHora } from '../utils/modificarHora'
import { modificarHoras } from '../utils/modificarHoras'
import { useCategoriasStore } from './categoriasStore'
import { resumenDia } from '@/utils/resumenDia'

interface DiasState {
  diaDetail: DiaReadDetail | null
  diasResumen: DiaResumen[]

  traerDiasResumen: () => Promise<void>
  traerDiaDetail: () => Promise<void>
  actualizarDia: (fechaISO: string, dia: DiaUpdate) => Promise<void>
  reordenarBloques: (event: DragEndEvent) => Promise<void>
  crearBloque: (idRef?: number) => Promise<void>
  actualizarBloque: (id: number, bloque: BloqueUpdate) => Promise<void>
  eliminarBloque: (id: number) => Promise<void>
  actualizarHoras: (idRef: number, duracion: number) => void
}

export const useDiasStore = create<DiasState>(set => {
  const actualizarResumen = (
    state: DiasState,
    diaDetail: DiaReadDetail
  ): DiaResumen[] =>
    state.diasResumen.map(diaResumen =>
      diaResumen.fecha === diaDetail.fecha
        ? resumenDia(diaDetail, useCategoriasStore.getState().categoriasDetail)
        : diaResumen
    )

  return {
    diaDetail: null,
    diasResumen: [],

    traerDiasResumen: async () => {
      const fecha = useFechaStore.getState().fecha
      const inicio = new Date(fecha.getFullYear(), fecha.getMonth(), 1)
      const final = new Date(fecha.getFullYear(), fecha.getMonth() + 1, 0)
      try {
        const data = await readDiasResumen(
          formatFechaISO(inicio),
          formatFechaISO(final)
        )
        set({ diasResumen: data })
      } catch (err) {
        console.error('Error al cargar rango de dias', err)
        set({ diasResumen: [] })
      }
    },

    traerDiaDetail: async () => {
      const fecha = useFechaStore.getState().fecha
      const fechaISO = formatFechaISO(fecha)
      try {
        const data = await readDiaDetail(fechaISO)
        set({ diaDetail: data })
      } catch (err) {
        console.error('Error al cargar el dia', err)
        set({ diaDetail: null })
      }
    },

    actualizarDia: async (fechaISO, dia) => {
      try {
        const newDia = await updateDia(fechaISO, dia)
        set(state => ({
          dia: newDia,
          // Al diaDetail le cambiamos solo los valores de dia
          diaDetail: state.diaDetail ? { ...state.diaDetail, ...newDia } : null,
          // Al diaResumen si está, lo buscamos y le cambiamos solo los valores de dia
          diasResumen: state.diasResumen.map(diaResumen =>
            diaResumen.fecha === fechaISO
              ? { ...diaResumen, ...newDia }
              : diaResumen
          ),
        }))
      } catch (err) {
        console.error('Error al actualizar el dia', err)
      }
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
        const fecha = useFechaStore.getState().fecha
        const fechaISO = formatFechaISO(fecha)
        const ids = bloques.map(bloque => bloque.id)
        const bloques_new = await sortDia(fechaISO, ids)
        set(state => {
          // Si por una casualidad no existe el diaDetail
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

    crearBloque: async idRef => {
      const fecha = useFechaStore.getState().fecha
      const fechaISO = formatFechaISO(fecha)
      try {
        const bloque = await createBloque({
          fecha: fechaISO,
          id_ref: idRef,
        })
        set(state => {
          // Si no existe creamos el dia falso confiando en que el backend
          if (!state.diaDetail) {
            const diaDetail = {
              fecha: fechaISO,
              titulo: null,
              estado: null,
              bloques: [bloque],
            }
            return {
              diaDetail,
              // Como diaDetail es falso, si usamos el actualizar no lo encuentra, usamos el resumenDia directamente
              diasResumen: [
                ...state.diasResumen,
                resumenDia(
                  diaDetail,
                  useCategoriasStore.getState().categoriasDetail
                ),
              ],
            }
          }

          // Para el button de ListaBloques
          const bloques = state.diaDetail.bloques
          if (idRef === undefined) {
            const diaDetail = {
              ...state.diaDetail,
              bloques: [...bloques, bloque],
            }
            return {
              diaDetail,
              diasResumen: actualizarResumen(state, diaDetail),
            }
          }

          const indiceRef = bloques.findIndex(bloque => bloque.id === idRef)
          const anteriores = bloques.slice(0, indiceRef + 1) // Incluido
          const siguientes = bloques.slice(indiceRef + 1)

          const newBloques = [
            ...anteriores,
            bloque,
            ...modificarHoras(siguientes, 0, bloque.duracion),
          ]
          const diaDetail = { ...state.diaDetail, bloques: newBloques }
          return {
            diaDetail,
            diasResumen: actualizarResumen(state, diaDetail),
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
          // Si por una casualidad no existe el diaDetail
          if (!state.diaDetail) return state
          const diaDetail = {
            // Conservamos título, estado y fecha
            ...state.diaDetail,
            bloques: state.diaDetail.bloques.map(bloque =>
              bloque.id === id ? { ...bloque, ...bloqueUpdate } : bloque
            ),
          }
          return {
            diaDetail,
            diasResumen: actualizarResumen(state, diaDetail),
          }
        })
      } catch (err) {
        console.error('Error actualizando el bloque', err)
        // TODO: Por si falla podriamos usar el get para un backup
      }
    },

    eliminarBloque: async (id: number) => {
      set(state => {
        // Si por una casualidad no existe el diaDetail
        if (!state.diaDetail) return state
        const bloques = state.diaDetail.bloques
        const indiceRef = bloques.findIndex(bloque => bloque.id === id)
        if (indiceRef === -1) return state

        const newBloques = bloques.filter(bloque => bloque.id !== id)
        const duracion = bloques[indiceRef].duracion
        const isLast = indiceRef === bloques.length - 1
        const diaDetail = {
          ...state.diaDetail,
          bloques: isLast
            ? newBloques
            : modificarHoras(newBloques, indiceRef, -duracion),
        }
        return {
          diaDetail,
          diasResumen: actualizarResumen(state, diaDetail),
        }
      })

      try {
        await deleteBloque(id)
      } catch (err) {
        console.error('Error eliminando el bloque', err)
      }
    },

    actualizarHoras: (id, duracion) => {
      set(state => {
        if (!state.diaDetail) return state
        const bloques = state.diaDetail.bloques
        const indiceRef = bloques.findIndex(bloque => bloque.id === id)
        if (indiceRef === -1) return state

        const diferencia = duracion - bloques[indiceRef].duracion

        // Si la diferencia es la misma
        if (diferencia === 0) return state

        const newBloques = [...bloques]
        newBloques[indiceRef] = {
          ...bloques[indiceRef],
          duracion,
          hora_fin: modificarHora(bloques[indiceRef].hora, duracion),
        }

        const diaDetail = {
          ...state.diaDetail,
          bloques: modificarHoras(newBloques, indiceRef + 1, diferencia),
        }
        return {
          diaDetail,
          diasResumen: actualizarResumen(state, diaDetail),
        }
      })
    },
  }
})
