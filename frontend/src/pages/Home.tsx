import CalendarioHeader from '../components/CalendarioHeader'
import Day from '../components/Day'
import ListaActividades from '../components/ListaActividades'

export default function Home() {
  return (
    <div className='h-full overflow-hidden flex justify-between'>
      <ListaActividades />
      <CalendarioHeader />
      <Day />
    </div>
  )
}
