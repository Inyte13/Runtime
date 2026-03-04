export interface ActividadCreate {
  nombre: string
  color?: string
  is_active?: boolean
}

  id: number
}

export interface ActividadUpdate {
  nombre?: string | null
  color?: string | null
  is_active?: boolean | null
}
