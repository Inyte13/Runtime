import { BloqueResponse } from './bloque'
import { CategoriaResumen } from './category'

export interface DiaResponse {
  fecha: string
  titulo: string | null
}

export interface DiaResponseDetail extends DiaResponse {
  bloques: BloqueResponse[]
}

export interface DiaResumen extends DiaResponse {
  categorias: CategoriaResumen[]
}

export interface DiaUpdate {
  titulo?: string | null
}
