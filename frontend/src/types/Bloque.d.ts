import { Actividad, ActividadRead } from './Actividad'
import { Dia } from './Dia'

export interface BloqueBase {
  hora: string
  descripcion?: string | null
  id_actividad: number
  duracion?: number | null
  hora_fin?: string | null
}

export interface Bloque extends BloqueBase {
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
