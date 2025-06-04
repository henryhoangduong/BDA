import { SimbaDoc } from '@/types/document'
import { API } from './axios-client'
import { config } from '@/config/config'
import { data } from 'react-router-dom'

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
export const ingestionByIdQueryFn = async (doc_id: string): Promise<SimbaDoc> => {
  const res = await API.get(`ingestion/${doc_id}`)
  return res.data
}
export const ingestionTasksQueryFn = async () => {
  const res = await API.put('')
  return res.data
}
export const ingestionDeleteMutationFn = async (doc_ids: string[]) => {
  const res = await API.delete(`ingestion`, { data: doc_ids })
  return res.data
}
//***************************** CHAT *****************************
export async function sendMessage(message: string): Promise<Response> {
  try {
    const response = await fetch(`${config.apiUrl}chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

export async function handleChatStream(
  response: Response,
  onChunk: (content: string, state: any) => void,
  onComplete: () => void
): Promise<void> {
  const reader = response.body?.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  console.log('🔄 Starting stream handling...')

  try {
    while (reader) {
      const { value, done } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      buffer += chunk

      // Split buffer by double newlines and process complete messages
      const messages = buffer.split('\n\n')
      buffer = messages.pop() || '' // Keep the last incomplete chunk in buffer

      for (const message of messages) {
        if (!message.trim()) continue

        try {
          // Remove 'data: ' prefix if it exists
          const jsonStr = message.replace(/^data: /, '')
          // console.log('📦 Raw chunk:', jsonStr)

          const data = JSON.parse(jsonStr)
          console.log('🔍 Parsed data:', data)

          if (data.error) {
            console.error('❌ Stream error:', data.error)
            continue
          }

          // Pass both content and state to the callback
          if (data.content !== undefined) {
            // console.log('📝 Content update:', { content: data.content, state: data.state })
            onChunk(data.content, data.state)
          } else if (data.state) {
            // console.log('🔄 State-only update:', data.state)
            onChunk('', data.state)
          }
        } catch (e) {
          console.error('❌ Error parsing stream chunk:', e)
        }
      }
    }
  } finally {
    console.log('✅ Stream handling complete')
    reader?.releaseLock()
    onComplete()
  }
}

//***************************** DATABASE *****************************
//***************************** EMBEDDING *****************************
export const embeddingDocumentByIdMutationFn = async (doc_id: string) => {
  const res = await API.post(`embed/document/${doc_id}`)
  return res.data
}
//***************************** PARSING *****************************
export const parseDocMutationFn = async (document_id: string, parser = 'docling') => {
  const response = await API.post('parses', { document_id: document_id, parser })
  return response.data
}
export const getParsersQueryFn = async () => {
  const response = await API.get('parsers')
  return response.data
}
export const getParsingTasksQueryFn = async () => {
  const response = await API.get('parsing/tasks')
  return response.data
}
export const getParsingTaskStatusByIdQueryFn = async (task_id: string) => {
  const response = await API.get(`parsing/tasks/${task_id}`)
  return response.data
}
