import { z } from 'zod'

export const category = z.object({
  name: z.string().min(2).max(25),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, 'Color hexadecimal inválido'),
})

export type Category = z.output<typeof category>
