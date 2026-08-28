import { z } from 'zod'

export const activity = z.object({
  name: z.string().min(2).max(25),
  category_id: z.uuid(),
})

export type Activity = z.output<typeof activity>
