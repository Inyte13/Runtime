import { queryClient } from '@/lib/query-client'
import { categoriaKeys } from '@/queries/category-queries'
import { Activity } from '@/schemas/activity-schema'
import {
  createActivity,
  deleteActivity,
  updateActivity,
} from '@/services/activity-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateActivity() {
  return useMutation({
    mutationFn: createActivity,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoriaKeys.detail() })
    },
  })
}

export function useUpdateActivity(id: string) {
  return useMutation({
    mutationFn: (activity: Activity) => updateActivity(id, activity),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoriaKeys.detail() })
    },
  })
}

export function useDeleteActivity(id: string) {
  return useMutation({
    mutationFn: () => deleteActivity(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: categoriaKeys.detail() })
    },
  })
}
