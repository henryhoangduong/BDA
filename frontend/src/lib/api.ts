import { SimbaDoc } from '@/types/document'
import { API } from './axios-client'

//***************************** INGESTION *****************************
export const ingestionMutationFn = async (files: FormData[]) => {
  const form = new FormData()
  Array.from(files).forEach((file) => {
    form.append('files', file)
  })

  const res = await API.post('ingestion', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    withCredentials: true
  })

  return res.data
}
export const ingestionQueryFn = async (): Promise<SimbaDoc[]> => {
  const res = await API.get('ingestion')
  return res.data
}
export const ingestionByIdQueryFn = async () => {
  const res = await API.get('')
  return res.data
}
export const ingestionTasksQueryFn = async () => {
  const res = await API.put('')
  return res.data
}

//***************************** CHAT *****************************

//***************************** DATABASE *****************************
