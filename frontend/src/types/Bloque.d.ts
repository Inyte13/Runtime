export interface BloqueCreate {
  duracion?: number
  descripcion?: string | null
  id_actividad?: number
  fecha: string
  id_ref?: number
}

export interface BloqueRead {
  id: number
  hora: string
  descripcion: string | null
  id_actividad: number
  duracion: number
  hora_fin: string
}

export interface BloqueUpdate {
  descripcion?: string | null
  id_actividad?: number
  duracion?: number
}
