import { Activity } from '@/schemas/activity-schema'
import { ActivityResponse, ActivityResponseDetail } from '../types/activity'
import { apiClient } from './api-client'

const URL = '/activities'

export async function createActivity(
  activity: Activity
): Promise<ActivityResponseDetail> {
  return apiClient<ActivityResponseDetail>(URL, {
    method: 'POST',
    body: JSON.stringify(activity),
  })
}

export async function updateActivity(
  id: string,
  activity: Activity
): Promise<ActivityResponse> {
  return apiClient<ActivityResponse>(`${URL}/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(activity),
  })
}

export async function deleteActivity(id: string): Promise<void> {
  return apiClient<void>(`${URL}/${id}`, {
    method: 'DELETE',
  })
}
