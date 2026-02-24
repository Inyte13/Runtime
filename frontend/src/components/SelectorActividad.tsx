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

    await actualizarBloque(bloque.id, { id_actividad: actividad.id })
    setColor(actividad.id, actividad.color)
  }


  return (
  )
}
