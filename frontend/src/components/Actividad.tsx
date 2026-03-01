import { memo } from "react";
import { ActividadRead } from "../types/Actividad";
import ColorPicker from "./ColorPicker";

export default function Actividad({ actividad }: { actividad: ActividadRead}) {
  const nombreBd = actividad.nombre
  const nombre = nombreBd.charAt(0).toUpperCase() + nombreBd.slice(1)
  return (
    <div className='flex items-center gap-2 p-1.5 hover:bg-accent hover:text-accent-foreground cursor-pointer rounded-lg'>
      <ColorPicker actividad={actividad} />
      <span>{nombre}</span>
    </div>
  )
}