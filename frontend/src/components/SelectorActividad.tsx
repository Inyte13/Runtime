import { useActividadesStore } from '../store/actividadesStore.js'
import { useDiasStore } from '../store/diasStore.js'
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
import { memo, useMemo } from 'react'
import { useShallow } from 'zustand/react/shallow'

export default memo(function SelectorActividad({ id }: { id: number }) {
  const actividad = useDiasStore(
    useShallow(
      state =>
        state.diaDetail?.bloques.find(bloque => bloque.id === id)?.actividad
    )
  )
  const actividad = useActividadesStore(state =>
    state.actividadesDetail.find(
      actividad => actividad.id === bloque?.id_actividad
    )
  )! // non-null assertion seguro por el loading en App
  
  const actualizarBloque = useDiasStore(state => state.actualizarBloque)
  const actividades = useActividadesStore(state => state.actividadesDetail)
  const color = useColorStore(
    state => state.colores[actividad.id] || actividad.color
  )

  // Puede ser null al limpiar con el btn X
  const manejarSelector = async (idStr: string | null) => {
    if (!idStr) return
    await actualizarBloque(id, { id_actividad: parseInt(idStr) })
  }

  // label y value son nombres que espera Base UI
  const items = useMemo(
    () =>
      actividades.map(act => ({
        label: act.nombre,
        value: act.id.toString(),
        color: act.color,
        isActive: act.is_active,
      })),
    [actividades]
  )

  return (
    <Combobox
      items={items}
      onValueChange={manejarSelector}
      value={actividad?.id.toString()}
    >
      <ComboboxTrigger
        render={
          <Button variant='ghost' className='p-1! gap-1'>
            <div className='flex items-center gap-2'>
              {actividad && (
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

      <ComboboxContent className='w-[17ch] text-popover-foreground'>
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
            <ComboboxItem
              key={item.value}
              value={item.value}
              className='py-1'
              disabled={!item.isActive}
            >
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
})
