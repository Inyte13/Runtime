import { create } from 'zustand'

export const useFechaStore = create((set) => ({
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
  })
}))
