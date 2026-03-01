import { create } from 'zustand'

interface ColorState {
  colores: Record<number, string>
  setColor: (id: number, color: string) => void
  setColores: (actividades: { id: number; color: string }[]) => void
}

export const useColorStore = create<ColorState>(set => ({
  colores: {},
  setColor: (id, color) =>
    // Solo cambiamos el color que cambia
    set(state => ({
      colores: { ...state.colores, [id]: color },
    })),
  setColores: actividades => {
    set({
      // Transforma en diccionario solo con id y color
      colores: Object.fromEntries(
        actividades.map(actividad => [actividad.id, actividad.color])
      ),
    })
  },
}))
