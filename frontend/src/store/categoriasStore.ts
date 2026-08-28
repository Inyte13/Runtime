import { create } from 'zustand'
import { ActividadCreate, ActividadUpdate } from '../types/activity'
import { useColorStore } from './colorStore'
import {
  CategoriaCreate,
  CategoriaReadDetail,
  CategoriaUpdate,
} from '@/types/category'
import {
  createCategoria,
  deleteCategoria,
  readCategoriasDetail,
  updateCategoria,
} from '@/services/category-service'
import {
  createActividad,
  deleteActividad,
  updateActividad,
} from '@/services/activity-service'

interface CategoriasState {
  categoriasDetail: CategoriaReadDetail[]
  traerCategoriasDetail: () => Promise<void>
  crearCategoria: (categoriaNew: CategoriaCreate) => Promise<void>
  actualizarCategoria: (
    id: number,
    categoriaNew: CategoriaUpdate
  ) => Promise<void>
  eliminarCategoria: (id: number) => Promise<void>
  crearActividad: (actividadNew: ActividadCreate) => Promise<void>
  actualizarActividad: (
    id: number,
    actividadNew: ActividadUpdate
  ) => Promise<void>
  eliminarActividad: (id: number) => Promise<void>
}

export const useCategoriasStore = create<CategoriasState>(set => ({
  categoriasDetail: [],

  traerCategoriasDetail: async () => {
    try {
      const data = await readCategoriasDetail()
      set({ categoriasDetail: data })
      // Store Hydration: Para guardar los los colores para no repetirlos
      useColorStore.getState().setColores(data)
    } catch (err) {
      console.error('Error al cargar las categorias', err)
    }
  },

  // Si cambias el #A18072, cambialo en el backend (categoria.py) models y schemas
  crearCategoria: async (categoriaNew: CategoriaCreate) => {
    // Optimistic update
    const idTemp = -Date.now()
    set(state => ({
      categoriasDetail: [
        ...state.categoriasDetail,
        {
          id: idTemp,
          nombre: categoriaNew.nombre,
          color: '#A18072',
          actividades: [],
        },
      ],
    }))

    try {
      const categoria = await createCategoria(categoriaNew)
      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail =>
          categoriaDetail.id === idTemp
            ? { ...categoria, actividades: [] }
            : categoriaDetail
        ),
      }))
    } catch (err) {
      console.error('Error al crear la categoria', err)
      set(state => ({
        categoriasDetail: state.categoriasDetail.filter(
          categoriaDetail => categoriaDetail.id !== idTemp
        ),
      }))
    }
  },

  actualizarCategoria: async (id, categoriaNew) => {
    try {
      const categoria = await updateCategoria(id, categoriaNew)
      // Si solo cambiaste color no hagas nada mas
      if (Object.keys(categoriaNew).every(k => k === 'color')) return
      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail =>
          categoriaDetail.id == id
            ? { ...categoriaDetail, ...categoria }
            : categoriaDetail
        ),
      }))
    } catch (err) {
      console.error('Error al actualizar la categoria', err)
    }
  },

  eliminarCategoria: async id => {
    try {
      await deleteCategoria(id)
      set(state => ({
        categoriasDetail: state.categoriasDetail.filter(
          categoriaDetail => categoriaDetail.id !== id
        ),
      }))
      useColorStore.getState().eliminarColor(id)
    } catch (err) {
      console.error('Error al eliminar la categoria', err)
    }
  },

  crearActividad: async actividadNew => {
    // Optimistic update
    const idTemp = -Date.now()
    set(state => ({
      categoriasDetail: state.categoriasDetail.map(categoriaDetail =>
        categoriaDetail.id === actividadNew.id_categoria
          ? {
              ...categoriaDetail,
              actividades: [
                ...categoriaDetail.actividades,
                {
                  id: idTemp,
                  nombre: actividadNew.nombre,
                  is_active: true,
                  tiene_bloques: false,
                },
              ],
            }
          : categoriaDetail
      ),
    }))
    try {
      const actividad = await createActividad(actividadNew)
      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail =>
          categoriaDetail.id === actividadNew.id_categoria
            ? {
                ...categoriaDetail,
                actividades: categoriaDetail.actividades.map(act =>
                  act.id === idTemp ? actividad : act
                ),
              }
            : categoriaDetail
        ),
      }))
    } catch (err) {
      console.error('Error al crear la actividad', err)
      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail =>
          categoriaDetail.id === actividadNew.id_categoria
            ? {
                ...categoriaDetail,
                actividades: categoriaDetail.actividades.filter(
                  act => act.id !== idTemp
                ),
              }
            : categoriaDetail
        ),
      }))
    }
  },

  actualizarActividad: async (id, actividadNew) => {
    try {
      const actividad = await updateActividad(id, actividadNew)

      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail => {
          // Verificamos si la actividad está en esa categoría
          const tieneActividad = categoriaDetail.actividades.some(
            actividad => actividad.id === id
          )
          if (!tieneActividad) return categoriaDetail
          // Si está en la categoria, la buscamos y reemplazamos solo los campos mandados
          return {
            ...categoriaDetail,
            actividades: categoriaDetail.actividades.map(actividadDetail =>
              actividadDetail.id === id
                ? { ...actividadDetail, ...actividad }
                : actividadDetail
            ),
          }
        }),
      }))
    } catch (err) {
      console.error('Error al actualizar la actividad', err)
    }
  },

  eliminarActividad: async id => {
    try {
      await deleteActividad(id)
      set(state => ({
        categoriasDetail: state.categoriasDetail.map(categoriaDetail => {
          // Verificamos si la actividad está en esa categoría
          const tieneActividad = categoriaDetail.actividades.some(
            actividadDetail => actividadDetail.id === id
          )
          if (!tieneActividad) return categoriaDetail
          // Si está en la categoria, la buscamos y la eliminamos
          return {
            ...categoriaDetail,
            actividades: categoriaDetail.actividades.filter(
              actividadDetail => actividadDetail.id !== id
            ),
          }
        }),
      }))
    } catch (err) {
      console.error('Error al eliminar la actividad', err)
    }
  },
}))
