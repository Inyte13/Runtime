import { useEffect, useRef } from "react";
import { useDiasStore } from "../store/diasStore";
import { useFechaStore } from "../store/fechaStore";
import { formatFechaDetail, formatFechaISO } from "../utils/formatDate";
import { Input } from "./ui/input";

export default function DiaHeader() {
  const fecha = useFechaStore(state => state.fecha)
  const fechaISO = formatFechaISO(fecha)
  const fechaDetail = formatFechaDetail(fecha)
  // (|| ''): Lo usamos porque un dia puede tener el titulo null
  // (?.): Lo usamos porque diaDetail puede no estar creado
  const titulo = useDiasStore(state => state.diaDetail?.titulo) || ''
  const actualizarDia = useDiasStore(state => state.actualizarDia)

    // Creame una ref pero por ahora es null
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // El input ya existe en HTML?
    if (inputRef.current) {
      // Usa el valor de la bd
      inputRef.current.value = titulo
    }
  }, [titulo])

  const manejarTitulo = async () => {
    // inputRef.current? puede ser undefinded
    const newTitulo = inputRef.current?.value || ''
    // Si es igual no hace nada
    if (newTitulo === titulo) return
    // Actualiza a la bd
    await actualizarDia(fechaISO, { titulo: newTitulo })
  }

  return (
    <header className='flex flex-col gap-y-1 items-center'>
      <h2 className='text-2xl font-semibold'>{fechaDetail}</h2>
      <Input
        ref={inputRef} // 4. Conectamos la referencia al componente
        className='text-center text-base italic border-0'
        defaultValue={titulo} // Solo se lee la primera vez
        placeholder='Añadir título'
        onBlur={manejarTitulo}
        maxLength={150}
      />
    </header>
  )
}
