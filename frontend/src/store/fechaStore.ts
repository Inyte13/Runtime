import { create } from 'zustand'

export interface FechaState {
  fecha: Date
  setFecha: (date: Date) => void
  prevDia: () => void
  nextDia: () => void
  irHoy: () => void
  getFechaISO: () => string
  getFechaTitle: () => string
  getFechaDetail: () => string
}

export const useFechaStore = create<FechaState>((set, get) => ({
  fecha: new Date(),
  setFecha: (date) => set({ fecha: date }),
  prevDia: () => set(state => {
    return {
      fecha: new Date(
        state.fecha.getFullYear(),
        state.fecha.getMonth(),
        state.fecha.getDate() - 1
      )
    }
  }),
  nextDia: () => set(state => {
    return {
      fecha: new Date(
        state.fecha.getFullYear(),
        state.fecha.getMonth(),
        state.fecha.getDate() + 1
      )
    }
  }),
  irHoy: () => set({
    fecha: new Date()
  }),
  getFechaISO: () => {
    return get().fecha.toLocaleDateString('sv-SE')
  },
  getFechaTitle: () => {
    return get().fecha
      .toLocaleDateString('es-ES', {
        month: 'long',
        year: 'numeric'
      })
    // El primer char a uppercase
      .replace(/^./, c => c.toUpperCase())
      .replace(/ de /g, ' ')
  },
  getFechaDetail: () => {
    return get().fecha
      .toLocaleDateString('es-ES', {
        weekday: 'long',
        day: 'numeric',
        month: 'short'
      })
      .replace(/^./, c => c.toUpperCase())
  }

}))
