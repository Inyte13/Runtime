import { ActivityResponseDetail, ActivityResume } from './activity'

export interface CategoryResponse {
  id: string
  name: string
  color: string
}

export interface CategoryResponseDetail extends CategoryResponse {
  activities: ActivityResponseDetail[]
  deletable: boolean
}

export interface CategoryResume {
  id: string
  activities: ActivityResume[]
}
