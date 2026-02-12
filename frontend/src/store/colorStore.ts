import { create } from 'zustand'

interface ColorState {
  colores: Record<number, string>
  setColor: (id: number, color: string) => void
}

export const useColorStore = create<ColorState>(set => ({
  colores: {},
  setColor: (id, color) =>
    set(state => ({
      colores: { ...state.colores, [id]: color },
    })),
}))
