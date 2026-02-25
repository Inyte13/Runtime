import { Combobox as ComboboxPrimitive } from '@base-ui/react'
import { CheckIcon, ChevronDown, XIcon } from 'lucide-react'
import { cn } from '../../lib/utils'
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from './input-group'
import React from 'react'
import { Button } from './button'
export const Combobox = ComboboxPrimitive.Root

// Para inyectarle el data-slot
export function ComboboxValue({ ...props }: ComboboxPrimitive.Value.Props) {
  return <ComboboxPrimitive.Value data-slot='combobox-value' {...props} />
}

// La flechita de la derecha, si se usa con render, solo usamos sus funciones
export function ComboboxTrigger({
  className,
  children,
  ...props
}: ComboboxPrimitive.Trigger.Props) {
  return (
    <ComboboxPrimitive.Trigger
      data-slot='combobox-trigger'
      className={cn("[&_svg:not([class*='size-'])]:size-4", className)}
      {...props}
    >
      {children}
      <ChevronDown
        data-slot='combobox-trigger-icon'
        className='text-muted-foreground pointer-events-none size-4'
      />
    </ComboboxPrimitive.Trigger>
  )
}
// Para limpiar el input
export function ComboboxClear({
  className,
  ...props
}: ComboboxPrimitive.Clear.Props) {
  return (
    <ComboboxPrimitive.Clear
      data-slot='combobox-clear'
      render={<InputGroupButton variant='ghost' size='icon-xs' />}
      className={cn(className)}
      {...props}
    >
      <XIcon className='pointer-events-none' />
    </ComboboxPrimitive.Clear>
  )
}
// Si existen el clear y el trigger agregamos el addon, y w-auto
export function ComboboxInput({
  className,
  children,
  disabled = false,
  showTrigger = true,
  showClear = false,
  ...props
}: ComboboxPrimitive.Input.Props & {
  showTrigger?: boolean
  showClear?: boolean
}) {
  return (
    <InputGroup className={cn('w-auto', className)}>
      <ComboboxPrimitive.Input
        render={<InputGroupInput disabled={disabled} />}
        {...props}
      />
      {(showTrigger || showClear) && (
        <InputGroupAddon align='inline-end'>
          {showTrigger && (
            <InputGroupButton
              size='icon-xs'
              variant='ghost'
              asChild // Fusionate con el trigger
              data-slot='input-group-button'
              className='group-has-data-[slot=combobox-clear]/input-group:hidden data-pressed:bg-transparent'
              disabled={disabled}
            >
              <ComboboxTrigger />
            </InputGroupButton>
          )}
          {showClear && <ComboboxClear disabled={disabled} />}
        </InputGroupAddon>
      )}
      {children}
    </InputGroup>
  )
}

// El popover
export function ComboboxContent({
  className,
  side = 'bottom',
  sideOffset = 6,
  align = 'start',
  alignOffset = 0,
  anchor,
  ...props
}: ComboboxPrimitive.Popup.Props &
  Pick< // Filtrame solo estas props
    ComboboxPrimitive.Positioner.Props,
    'side' | 'align' | 'sideOffset' | 'alignOffset' | 'anchor'
  >) {
  return (
    <ComboboxPrimitive.Portal>
      <ComboboxPrimitive.Positioner
        side={side}
        sideOffset={sideOffset}
        align={align}
        alignOffset={alignOffset}
        anchor={anchor}
        className='isolate z-50'
      >
        <ComboboxPrimitive.Popup
          data-slot='combobox-content'
          data-chips={!!anchor}
          className={cn(
            'group/combobox-content bg-popover text-popover-foreground overflow-hidden rounded-md shadow-md relative max-h-96',
            'w-(--anchor-width)', // Se adapta al mismo ancho del InputGroupButton
            'max-w-(--available-width)', // Que no sea mas grande que la pantalla del usuario
            // 'min-w-[calc(var(--anchor-width)+--spacing(7))]', // Minimo adaptado mas los icons
            'origin-(--transform-origin)', // Si hay espacio debajo, el menú se abre hacia abajo. Si estás al final de la página, se abre hacia arriba
            'data-[chips=true]:min-w-(--anchor-width)', // Cambia el ancho por las chips
            'data-open:animate-in data-closed:animate-out data-closed:fade-out-0 data-open:fade-in-0 data-closed:zoom-out-95 data-open:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 duration-100 ',
            'ring-1 ring-ring', // Borde pero para popover
            '*:data-[slot=input-group]:bg-input/30', // Si esta el input le cambio el bg
            '*:data-[slot=input-group]:border-input/30',
            '*:data-[slot=input-group]:m-1',
            '*:data-[slot=input-group]:mb-0',
            '*:data-[slot=input-group]:h-8',
            '*:data-[slot=input-group]:shadow-none',
            className
          )}
          {...props}
          />
      </ComboboxPrimitive.Positioner>
    </ComboboxPrimitive.Portal>
  )
}

export function ComboboxList({
  className,
  ...props
}: ComboboxPrimitive.List.Props) {
  return (
    <ComboboxPrimitive.List
      data-slot='combobox-list'
      className={cn(
        'scroll-py-1 overflow-y-auto p-1 data-empty:p-0',
        'max-h-[min(calc(--spacing(96)---spacing(9)),calc(var(--available-height)---spacing(9)))]',
        className
      )}
      {...props}
    />
  )
}

// El tamaño debe ser igual que el input
export function ComboboxItem({
  className,
  children,
  ...props
}: ComboboxPrimitive.Item.Props) {
  return (
    <ComboboxPrimitive.Item
      data-slot='combobox-item'
      className={cn(
        "data-highlighted:bg-accent data-highlighted:text-accent-foreground relative flex w-full cursor-default items-center gap-2 rounded-sm py-1.5 pr-8 pl-2 text-base outline-hidden select-none data-disabled:pointer-events-none data-disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
        className
      )}
      {...props}
    >
      {children}
      <ComboboxPrimitive.ItemIndicator
        data-slot='combobox-item-indicator'
        render={
          <span className='pointer-events-none absolute right-2 flex size-4 items-center justify-center' />
        }
      >
        <CheckIcon className='pointer-events-none size-4 pointer-coarse:size-5' />
      </ComboboxPrimitive.ItemIndicator>
    </ComboboxPrimitive.Item>
  )
}

// Cuando quiero agrupar opciones separar visualmente
export function ComboboxGroup({
  className,
  ...props
}: ComboboxPrimitive.Group.Props) {
  return (
    <ComboboxPrimitive.Group
      data-slot='combobox-group'
      className={cn(className)}
      {...props}
    />
  )
}

// El titulo de un group
export function ComboboxLabel({
  className,
  ...props
}: ComboboxPrimitive.GroupLabel.Props) {
  return (
    <ComboboxPrimitive.GroupLabel
      data-slot='combobox-label'
      className={cn(
        'text-muted-foreground px-2 py-1.5 text-xs pointer-coarse:px-3 pointer-coarse:py-2 pointer-coarse:text-sm',
        className
      )}
      {...props}
    />
  )
}

// Idk
export function ComboboxCollection({
  ...props
}: ComboboxPrimitive.Collection.Props) {
  return (
    <ComboboxPrimitive.Collection data-slot='combobox-collection' {...props} />
  )
}

// Cuando no encuentra la busqueda
export function ComboboxEmpty({
  className,
  ...props
}: ComboboxPrimitive.Empty.Props) {
  return (
    <ComboboxPrimitive.Empty
      data-slot='combobox-empty'
      className={cn(
        'text-muted-foreground hidden w-full justify-center py-2 text-center text-sm group-data-empty/combobox-content:flex',
        className
      )}
      {...props}
    />
  )
}

// Cuando hay grupos los separa visualmente
export function ComboboxSeparator({
  className,
  ...props
}: ComboboxPrimitive.Separator.Props) {
  return (
    <ComboboxPrimitive.Separator
      data-slot='combobox-separator'
      className={cn('bg-border -mx-1 my-1 h-px', className)}
      {...props}
    />
  )
}

// Agrupa las selecciones cuando es un Combobox múltiple
export function ComboboxChips({
  className,
  ...props
}: React.ComponentPropsWithRef<typeof ComboboxPrimitive.Chips> &
  ComboboxPrimitive.Chips.Props) {
  return (
    <ComboboxPrimitive.Chips
      data-slot='combobox-chips'
      className={cn(
        'dark:bg-input/30 border-input has-aria-invalid:ring-destructive/20 dark:has-aria-invalid:ring-destructive/40 has-aria-invalid:border-destructive dark:has-aria-invalid:border-destructive/50 flex min-h-9 flex-wrap items-center gap-1.5 rounded-md border bg-transparent bg-clip-padding px-2.5 py-1.5 text-sm   has-aria-invalid:ring-[3px] has-data-[slot=combobox-chip]:px-1.5',
        'focus-within:ring-[3px] focus-within:border-ring focus-within:ring-ring/50',
        // 'shadow-xs transition-[color,box-shadow]',
        className
      )}
      {...props}
    />
  )
}

// Cada una de las pildoras
export function ComboboxChip({
  className,
  children,
  showRemove = true,
  ...props
}: ComboboxPrimitive.Chip.Props & {
  showRemove?: boolean
}) {
  return (
    <ComboboxPrimitive.Chip
      data-slot='combobox-chip'
      className={cn(
        'bg-muted text-foreground flex h-[calc(--spacing(5.5))] w-fit items-center justify-center gap-1 rounded-sm px-1.5 text-xs font-medium whitespace-nowrap has-disabled:pointer-events-none has-disabled:cursor-not-allowed has-disabled:opacity-50 has-data-[slot=combobox-chip-remove]:pr-0',
        className
      )}
      {...props}
    >
      {children}
      {showRemove && (
        <ComboboxPrimitive.ChipRemove
          render={<Button variant='ghost' size='icon-xs' />}
          className='-ml-1 opacity-50 hover:opacity-100'
          data-slot='combobox-chip-remove'
        >
          <XIcon className='pointer-events-none' />
        </ComboboxPrimitive.ChipRemove>
      )}
    </ComboboxPrimitive.Chip>
  )
}

// Una chips dinámica
export function ComboboxChipsInput({
  className,
  children,
  ...props
}: ComboboxPrimitive.Input.Props) {
  return (
    <ComboboxPrimitive.Input
      data-slot='combobox-chip-input'
      className={cn('min-w-16 flex-1 outline-none', className)}
      {...props}
    />
  )
}

export function useComboboxAnchor() {
  return React.useRef<HTMLDivElement | null>(null)
}
