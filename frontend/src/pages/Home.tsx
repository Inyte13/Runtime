import Calendario from '../components/Calendario'
import Dia from '../components/Dia'
import ListaActividades from '../components/ListaActividades'

export default function Home() {
  return (
    <div className='h-full overflow-hidden flex justify-between'>
      <ListaActividades />
      <Calendario />
      <Dia />
    </div>
  )
}
