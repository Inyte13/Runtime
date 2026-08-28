import { ApiError } from '@/services/errors'
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1 minute, default: 0, tiempo en el que se considera fresco la data
      // gcTime: 1000 * 60 * 5, // 5 minutes, garbage collection, se reinicia el temporizador cada vez que no se usa
      retry: 0, // Intentos por si falla
      // refetchOnWindowFocus: true,
      // refetchOnReconnect: true,
    },
  },
})

export function validateRetry(nroReintentos: number) {
  // La fn que llama tanstack cada vez que incrementa intentos
  return function reintentar(failureCount: number, error: unknown) {
    // failureCount: el contador de tanstack lo maneja y se autoincrementa, empieza en 1
    if (nroReintentos < 1) return false
    if (
      error instanceof ApiError &&
      400 <= error.status_code &&
      error.status_code < 500
    ) {
      return false
    }
    return failureCount <= nroReintentos
  }
}
