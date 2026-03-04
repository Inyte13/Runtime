import { KeyboardEvent } from 'react'

// Cuando pulse enter quite el blur/foco
export function manejarEnter (e: KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>) {
  if (e.key === 'Enter') {
    e.currentTarget.blur() 
  }
}