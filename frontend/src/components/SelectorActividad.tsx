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
} from './ui/combobox.js'
import { Button } from './ui/button.js'
import { ChevronDown } from 'lucide-react'

export default function SelectorActividad({ bloque }: { bloque: BloqueRead }) {
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const actividades = useActividadesStore(state => state.actividades)
  const color = useColorStore(
    state => state.colores[bloque.actividad.id] || bloque.actividad.color
  )

  const manejarSelector = async (id: string | null) => {
    if (!id) return
    const actividad = actividades.find(
      actividad => actividad.id.toString() === id
    )
    if (!actividad) return
    await actualizarBloque(bloque.id, { id_actividad: actividad.id })
  }

  const items = actividades.map(act => ({
    label: act.nombre,
    value: act.id.toString(),
    color: act.color,
  }))

  return (
    <Combobox
      items={items}
      onValueChange={manejarSelector}
      value={bloque.actividad?.id.toString()}
      // onOpenChange={isOpen => {
      //   if (isOpen && actividades.length === 0) traerActividades()
      // }}
    >
      <ComboboxTrigger
        render={
          <Button variant='ghost' className='p-1! gap-1'>
            <div className='flex items-center gap-2'>
              {bloque.actividad && (
                <span
                  className='size-4 rounded-full shrink-0'
                  style={{ backgroundColor: color }}
                />
              )}
              <span className='capitalize text-2xl font-light'>
                <ComboboxValue />
              </span>
            </div>
            <ChevronDown className='size-4 opacity-50' />
          </Button>
        }
      />

      <ComboboxContent className='w-[17ch] text-popover-foreground/90'>
        <ComboboxInput
          showTrigger={false}
          showClear={true}
          placeholder='Buscar'
        />

        <ComboboxEmpty className='py-4 text-center text-sm text-muted-foreground'>
          No se encontraron actividades
        </ComboboxEmpty>

        <ComboboxList className='[&::-webkit-scrollbar]:hidden [scrollbar-width:none] '>
          {item => (
            <ComboboxItem key={item.value} value={item.value} className='py-1'>
              <div className='flex items-center gap-2'>
                <span
                  className='size-3 rounded-full shrink-0'
                  style={{ backgroundColor: item.color }}
                />
                <span className='truncate capitalize'>{item.label}</span>
              </div>
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}
