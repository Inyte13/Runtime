import { ActividadResumen } from '@/types/activity'
import { CategoriaReadDetail, CategoriaResumen } from '@/types/category'
import { DiaReadDetail, DiaResumen } from '@/types/dia'

export function resumenDia(
  diaDetail: DiaReadDetail,
  categorias: CategoriaReadDetail[]
): DiaResumen {
  const categoriasMap: Record<number, CategoriaResumen> = {}
  const actividadesMap: Record<number, ActividadResumen> = {}

  for (const bloque of diaDetail.bloques) {
    const { id_actividad, descripcion, duracion } = bloque
    // Ignoramos id=6, harcodeado, actividad 'Dormir'
    if ([6].includes(id_actividad)) continue

    const id_categoria = categorias.find(categoria =>
      categoria.actividades.some(actividad => actividad.id === id_actividad)
    )?.id

    if (!id_categoria) continue

    if (!categoriasMap[id_categoria]) {
      categoriasMap[id_categoria] = { id: id_categoria, actividades: [] }
    }

    if (!actividadesMap[id_actividad]) {
      const actividad: ActividadResumen = {
        id: id_actividad,
        duracion,
        descripciones: descripcion ? [descripcion] : [],
      }
      actividadesMap[id_actividad] = actividad
      categoriasMap[id_categoria].actividades.push(actividad)
    } else {
      actividadesMap[id_actividad].duracion += duracion
      if (descripcion)
        actividadesMap[id_actividad].descripciones.push(descripcion)
    }
  }
  // Orden ascendente de las actividades
  Object.values(categoriasMap).forEach(categoria =>
    categoria.actividades.sort((a, b) => b.duracion - a.duracion)
  )
  return {
    fecha: diaDetail.fecha,
    titulo: diaDetail.titulo,
    estado: diaDetail.estado,
    categorias: Object.values(categoriasMap),
  }
}
