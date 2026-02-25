import ListaBloques from './ListaBloques'
import { useFechaStore } from '../store/fechaStore'
import { useEffect } from 'react'
import { useDiasStore } from '../store/diasStore'
import { Input } from './ui/input'

export default function Dia() {
  const fechaDetail = useFechaStore(state => state.getFechaDetail())
  const fechaISO = useFechaStore(state => state.getFechaISO())

  const fecha = useFechaStore(state => state.fecha)
  const diaDetail = useDiasStore(state => state.diaDetail)
  const bloques = diaDetail?.bloques || []

  const traerDiaDetail = useDiasStore(state => state.traerDiaDetail)
  const actualizarDia = useDiasStore(state => state.actualizarDia)
  
  useEffect(() => {
    traerDiaDetail()
  }, [fecha, traerDiaDetail])

  const manejarTitulo = async (e: React.FocusEvent<HTMLInputElement>) => {
    await actualizarDia(fechaISO, { titulo: e.target.value })
  }
  return (
    <section className='flex flex-col min-w-90 h-full gap-y-2 p-4' >
      <header className='flex flex-col gap-y-1 items-center'>
        <h2 className='text-2xl font-semibold'>{fechaDetail}</h2>
        <Input
          className='text-center text-base italic border-0'
          defaultValue={diaDetail?.titulo || ''}
          placeholder='Añadir título'
          onBlur={manejarTitulo}
          maxLength={150}
          disabled={diaDetail === null}
        />
      </header>
      <div className='flex-1 min-h-0'>
        <ListaBloques bloques={bloques} />
      </div>
    </section>
  )
}
