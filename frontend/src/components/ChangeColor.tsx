import { useCategoriasStore } from '../store/categoriasStore.js'
import { useColorStore } from '../store/colorStore.js'
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover.js'
import { Button } from './ui/button.js'
import { colores } from '@/utils/colors.js'
import { HexColorPicker } from 'react-colorful'
import { Separator } from './ui/separator.js'

export default function ChangeColor({
  id,
  colorFallback,
}: {
  id: number
  colorFallback: string
}) {
  const color = useColorStore(state => state.colores[id] || colorFallback)
  const setColor = useColorStore(state => state.setColor)
  const actualizarCategoria = useCategoriasStore(
    state => state.actualizarCategoria
  )
  return (
    <Popover
      onOpenChange={async open => {
        if (!open) {
          await actualizarCategoria(id, { color })
        }
      }}
    >
      <PopoverTrigger asChild>
        <Button
          className='size-4 rounded-full'
          size='icon'
          style={{ background: color }}
        />
      </PopoverTrigger>
      <PopoverContent
        side='top'
        align='start'
        className='flex w-44 flex-row items-center gap-x-1 p-1'
        sideOffset={8}
        alignOffset={0}
      >
        <ul className='flex overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden'>
          {colores.map(({ nombre, hex }) => (
            <li key={nombre} className='flex px-0.5 py-1'>
              <Button
                size='icon'
                className='size-4 rounded-full'
                style={{ background: hex }}
                onClick={() => setColor(id, hex)}
              />
            </li>
          ))}
        </ul>

        <Separator orientation='vertical' className='h-4 w-px' />

        <Popover>
          <PopoverTrigger asChild>
            <div data-slot='wrapper' className='ml-0.5 flex'>
              <Button
                className='size-4 rounded-full'
                size='icon'
                style={{ background: color }}
              />
            </div>
          </PopoverTrigger>
          <PopoverContent
            className='w-auto'
            side='right'
            align='start'
            sideOffset={16}
            alignOffset={-8}
            updatePositionStrategy='always'
          >
            <HexColorPicker
              color={color}
              onChange={newColor => setColor(id, newColor)}
            />
          </PopoverContent>
        </Popover>
      </PopoverContent>
    </Popover>
  )
}
