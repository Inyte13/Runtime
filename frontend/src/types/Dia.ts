import { Bloque, BloqueRead } from './Bloque'

export enum Estado {
  MAL = 1,
  NORMAL = 2,
  BIEN = 3
}

export interface DiaBase {
  titulo?: string | null,
  estado: Estado,
  fecha: string
}

export interface Dia extends DiaBase {
  bloques: Bloque[]
}

export type DiaCreate = DiaBase

export type DiaRead = DiaBase

export interface DiaReadDetail extends DiaRead {
  bloques: BloqueRead[]
}
export interface DiaUpdate {
  titulo?: string | null,
  estado?: Estado | null
}
