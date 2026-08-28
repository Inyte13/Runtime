import { CategoryResponse, CategoryResponseDetail } from '@/types/category'
import { apiClient } from './api-client'
import { Category } from '@/schemas/category-schema'

const URL = '/categories'

export async function getCategoriesDetail(): Promise<CategoryResponseDetail[]> {
  return apiClient<CategoryResponseDetail[]>(URL)
}

export async function createCategory(
  category: Category
): Promise<CategoryResponseDetail> {
  return apiClient<CategoryResponseDetail>(URL, {
    method: 'POST',
    body: JSON.stringify(category),
  })
}

export async function updateCategory(
  id: string,
  category: Category
): Promise<CategoryResponse> {
  return apiClient<CategoryResponse>(`${URL}/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(category),
  })
}

export async function deleteCategory(id: string): Promise<void> {
  return apiClient<void>(`${URL}/${id}`, {
    method: 'DELETE',
  })
}
