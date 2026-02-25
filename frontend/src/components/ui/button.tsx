import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'
import { Slot } from '@radix-ui/react-slot'

// Los valores por default
export const buttonVariants = cva(
  [
    'inline-flex items-center justify-center rounded-lg gap-2 ',
    'disabled:pointer-events-none disabled:opacity-50',
    'outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]',
    'whitespace-nowrap', // Mantenerse en una sola línea
    'shrink-0', // No me aplastes, yo mantengo mi tamaño
    // Para cualquier svg dentro
    '[&_svg]:pointer-events-none', // Evita que se haga click al svg, solo al btn
    '[&_svg]:shrink-0', // El icono mantiene su tamaño
    'transition-all',
    // 'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
  ],
  {
    variants: {
      variant: {
        primary: 'bg-primary text-primary-foreground hover:bg-primary/80',
        secondary:
          'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost:
          'hover:bg-accent/50 hover:text-accent-foreground',
        destructive:
          "bg-destructive text-white hover:bg-destructive/70 focus-visible:ring-destructive/20 ",
      },
      size: {
        xs: 'text-xs py-1 min-h-6 px-2 gap-1 has-[>svg]:px-1.5',
        sm: 'text-sm py-1.5 min-h-8 px-3 gap-1.5 has-[>svg]:px-2.5',
        md: 'text-sm py-2 min-h-9 px-4 font-medium has-[>svg]:px-3',
        lg: 'text-base py-2.5 min-h-10 px-6 has-[>svg]:px-4',
        'icon-xxs': 'size-5 [&_svg:not([class*="size-"])]:size-3',
        'icon-xs': 'size-6 [&_svg:not([class*="size-"])]:size-4',
        'icon-sm': 'size-8 [&_svg:not([class*="size-"])]:size-5',
        'icon-md': 'size-9 [&_svg:not([class*="size-"])]:size-6',
        'icon-lg': 'size-10 [&_svg:not([class*="size-"])]:size-7',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

export function Button({
  className,
  variant = 'primary',
  size = 'md',
  asChild = false,
  ...props
}: React.ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : 'button'
  return (
    <Comp
      // data-slot='button'
      // data-variant={variant}
      // data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

