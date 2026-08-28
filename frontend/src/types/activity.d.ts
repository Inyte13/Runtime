export interface ActivityResponse {
  id: string
  name: string
}

export interface ActivityResponseDetail extends ActivityResponse {
  deletable: boolean
}

export interface ActivityResume {
  id: number
  duration: number
  descriptions: string[]
}
