import { queryClient } from '@/lib/query-client'
import { categoryKeys } from '@/queries/category-queries'
import { Category } from '@/schemas/category-schema'
import {
  createCategory,
  deleteCategory,
  updateCategory,
} from '@/services/category-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateCategory() {
  return useMutation({
    mutationFn: createCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.detail() })
    },
  })
}

export function useUpdateCategory(id: string) {
  return useMutation({
    mutationFn: (category: Category) => updateCategory(id, category),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.detail() })
    },
  })
}

export function useDeleteCategory(id: string) {
  return useMutation({
    mutationFn: () => deleteCategory(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoryKeys.detail() })
    },
  })
}
