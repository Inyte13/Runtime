import { cn } from '../../lib/utils'

export function Input({
  className,
  type,
  ...props
}: React.ComponentProps<'input'>) {
  return (
    <input
      type={type}
      data-slot='input'
      className={cn(
        'placeholder:text-muted-foreground h-9 w-full min-w-0 bg-transparent outline-none',
        'disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50',
        'text-base transition-[color,box-shadow] shadow-xs',
        'border border-input rounded-md px-3 py-1', // Para el input vanilla
        
        // "file:text-foreground file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium",
        
        // "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        
        // "aria-invalid:ring-destructive/20 aria-invalid:border-destructive",
        
        // 'selection:bg-primary selection:text-primary-foreground', // Al seleccionar para copiar, ya lo uso en el global
        
        // 'md:text-sm', // Para moviles
        className
      )}
      {...props}
    />
  )
}
        
