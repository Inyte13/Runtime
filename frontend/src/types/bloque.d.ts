export interface BloqueCreate {
  duracion?: number // default: 0.5 en el backend
  descripcion?: string | null
  fecha: string
  id_actividad?: string
  id_ref?: string
}

export interface BloqueResponse {
  id: string
  hora: string
  hora_fin: string
  duracion: number
  descripcion: string | null
  id_actividad: string
}

export interface BloqueUpdate {
  duracion?: number
  descripcion?: string | null
  id_actividad?: string
}
