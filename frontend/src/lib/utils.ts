import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// cn === class names
export function cn(...inputs: ClassValue[]) {
  // twMerge es para eliminar las clases pasadas y no generar conflicto
  // clsx junta todas las clases y limpia los condicionales o nulos
  return twMerge(clsx(inputs))
}