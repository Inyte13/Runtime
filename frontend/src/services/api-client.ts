import { BASE_URL } from '@/lib/constants'
import { ApiError } from './errors'

export async function apiClient<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'applications/json',
      ...options?.headers,
    },
  })

  if (!res.ok) {
    const payload = await res.json().catch(() => ({
      code: 'UNKNOWN_ERROR',
      message: 'Error desconocido',
    }))
    throw new ApiError(res.status, payload.code, payload.message)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}
