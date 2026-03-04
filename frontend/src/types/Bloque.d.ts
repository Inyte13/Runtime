export interface BloqueRead {
  id: number
  hora: string
  descripcion: string | null
  actividad: ActividadRead
  duracion: number | null
  hora_fin: string | null
}

export interface BloqueCreate {
  hora?: string | null
  descripcion?: string | null
  id_actividad?: number | null
  fecha: string
  duracion?: number | null
}

export interface BloqueUpdate {
  descripcion?: string | null
  id_actividad?: number
  duracion?: number | null
}
