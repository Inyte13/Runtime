import { BloqueRead } from './Bloque'

export enum Estado {
  MAL = 1,
  NORMAL = 2,
  BIEN = 3,
}

export interface DiaRead {
  titulo: string | null
  estado: Estado | null
  fecha: string
}

export interface DiaReadDetail extends DiaRead {
  bloques: BloqueRead[]
}

export interface DiaUpdate {
  titulo?: string | null
  estado?: Estado | null
}
