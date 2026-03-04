  id: number
  fecha: string
  actividad?: Actividad | null
  dia: Dia
}

export interface BloqueCreate {
  hora?: string | null
  descripcion?: string | null
  id_actividad?: number | null
  fecha?: string | null
  duracion?: number | null
}
export interface BloqueRead {
  id?: number | null
  hora?: string | null
  descripcion?: string | null
  actividad?: ActividadRead | null
  duracion?: number | null
  hora_fin?: string | null
}

export interface BloqueUpdate {
  hora?: string | null
  descripcion?: string | null
  id_actividad?: number | null
  duracion?: number | null
}
