import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        // Para type='file'
        "file:text-foreground file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium",
        // "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        // Si el input tiene aria-invalid='true'
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        // Cuando esta disabled
        "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",

        "italic focus:border-b focus:border-gray text-gray-300",
        // "selection:bg-primary selection:text-primary-foreground px-3 dark:bg-input/30 md:text-sm",
        "placeholder:text-muted-foreground border-input h-9 w-full min-w-0 bg-transparent  shadow-xs transition-[color,box-shadow] outline-none",
        className
      )}
      {...props}
    />
  )
}

export { Input }
