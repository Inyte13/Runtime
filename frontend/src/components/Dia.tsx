import ListaBloques from './ListaBloques'
import { useFechaStore } from '../store/fechaStore'
import { useEffect } from 'react' // Importamos useRef en vez de useState
import { useDiasStore } from '../store/diasStore'
import DiaHeader from './DiaHeader'

export default function Dia() {
  const fecha = useFechaStore(state => state.fecha)
  const traerDiaDetail = useDiasStore(state => state.traerDiaDetail)
  useEffect(() => {
    traerDiaDetail()
  }, [fecha, traerDiaDetail])

  return (
    <section className='flex flex-col min-w-90 h-full gap-y-2 p-4'>
      <DiaHeader />
      <div className='flex-1 min-h-0'>
        <ListaBloques />
      </div>
    </section>
  )
}
