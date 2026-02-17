import { ActividadRead } from "../types/Actividad";
import ColorPicker from "./ColorPicker";

export default function Actividad({ actividad }: { actividad: ActividadRead}) {
  const nombreBd = actividad.nombre
  const nombre = nombreBd.charAt(0).toUpperCase() + nombreBd.slice(1)
  return (
    <article className='flex justify-star items-center gap-x-2'>
      <ColorPicker actividad={actividad} />
      <header>{nombre}</header>
    </article>
  )
}