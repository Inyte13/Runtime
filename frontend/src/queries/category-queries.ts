import { getCategoriesDetail } from '@/services/category-service'
import { queryOptions } from '@tanstack/react-query'

export const categoryKeys = {
  detail: () => ['categories', 'detail'] as const,
}

export function categoryOptions() {
  return queryOptions({
    queryKey: categoryKeys.detail(),
    queryFn: () => getCategoriesDetail(),
  })
}
