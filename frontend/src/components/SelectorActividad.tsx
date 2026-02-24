import { useActividadesStore } from '../store/actividadesStore.js'
import { useDiasStore } from '../store/diasStore.js'
import { BloqueRead } from '../types/Bloque.js'
import { useColorStore } from '../store/colorStore.js'
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
  ComboboxTrigger,
  ComboboxValue,
  useComboboxAnchor,
} from './ui/combobox.js'
import { ScrollArea } from './ui/scroll-area.js'
import { Button } from './ui/button.js'
import { ChevronDown } from 'lucide-react'

export default function SelectorActividad({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const actividades = useActividadesStore(state => state.actividades)
  const traerActividades = useActividadesStore(state => state.traerActividades)
  const setColor = useColorStore(state => state.setColor)
  const [selector, setSelector] = useState(false)
  const modalRef = useRef(null)

  useEffect(() => {
    const manejarClickOut = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        setSelector(false)
      }
    }
    document.addEventListener('mousedown', manejarClickOut)
    return () => document.removeEventListener('mousedown', manejarClickOut)
  }, [])

  const manejarSelector = async (actividad: ActividadRead) => {
    await actualizarBloque(bloque.id, { id_actividad: actividad.id })
    setColor(actividad.id, actividad.color)
  }

  const manejarClick = () => {
    if (!selector) {
      traerActividades()
    }
    setSelector(!selector)
  }

  return (
    <div ref={modalRef}>
      <button onClick={manejarClick}>
        <svg
          xmlns='http://www.w3.org/2000/svg'
          width='24'
          height='24'
          viewBox='0 0 24 24'
          fill='none'
          stroke='currentColor'
          strokeWidth='2'
          strokeLinecap='round'
          strokeLinejoin='round'
          className='icon icon-tabler icons-tabler-outline icon-tabler-menu-2'
        >
          <path stroke='none' d='M0 0h24v24H0z' fill='none' />
          <path d='M4 6l16 0' />
          <path d='M4 12l16 0' />
          <path d='M4 18l16 0' />
        </svg>
        {selector && (
          <div>
            <ul>
              {actividades.map(act => (
                <li key={act.id} onClick={() => manejarSelector(act)}>
                  <span style={{ background: act.color }} />
                  <a>
                    {act.nombre.charAt(0).toUpperCase() + act.nombre.slice(1)}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </button>
    </div>
  )
}
