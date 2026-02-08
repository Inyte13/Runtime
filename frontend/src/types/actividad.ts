export interface ActividadBase {
  nombre: string,
  color: string,
  is_active: boolean
}

export interface Actividad {
  id: number
}

export type ActividadCreate = ActividadBase

export interface ActividadRead extends ActividadBase {
  id: number
}

export interface ActividadUpdate {
  nombre?: string | null,
  color?: string | null,
  is_active?: boolean | null
}
