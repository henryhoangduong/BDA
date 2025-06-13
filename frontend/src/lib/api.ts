import { API } from './axios-client'

import { config } from '@/config/config'
import { User } from '@/types/auth'
import { SimbaDoc } from '@/types/document'

//*********************************************************************
//***************************** INGESTION *****************************
//*********************************************************************
const ingestionMutationFn = async (files: FormData[]) => {
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
const ingestionQueryFn = async (): Promise<SimbaDoc[]> => {
  const res = await API.get('ingestion')
  return res.data
}
const ingestionByIdQueryFn = async (doc_id: string): Promise<SimbaDoc> => {
  const res = await API.get(`ingestion/${doc_id}`)
  return res.data
}
const ingestionTasksQueryFn = async () => {
  const res = await API.put('')
  return res.data
}
const ingestionDeleteMutationFn = async (doc_ids: string[]) => {
  const res = await API.delete(`ingestion`, { data: doc_ids })
  return res.data
}

//*********************************************************************
//***************************** CHAT **********************************
//*********************************************************************
const sendMessage = async (message: string): Promise<Response> => {
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

const handleChatStream = async (
  response: Response,
  onChunk: (content: string, state: any) => void,
  onComplete: () => void
): Promise<void> => {
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
//*********************************************************************
//***************************** DATABASE ******************************
//*********************************************************************

//*********************************************************************
//***************************** EMBEDDING *****************************
//*********************************************************************
const embeddingDocumentByIdMutationFn = async (doc_id: string) => {
  const res = await API.post(`embed/document/${doc_id}`)
  return res.data
}

//*********************************************************************
//***************************** PARSING *******************************
//*********************************************************************
const parseDocMutationFn = async (document_id: string, parser = 'docling') => {
  const response = await API.post('parses', { document_id: document_id, parser })
  return response.data
}
const getParsersQueryFn = async () => {
  const response = await API.get('parsers')
  return response.data
}
const getParsingTasksQueryFn = async () => {
  const response = await API.get('parsing/tasks')
  return response.data
}
const getParsingTaskStatusByIdQueryFn = async (task_id: string) => {
  const response = await API.get(`parsing/tasks/${task_id}`)
  return response.data
}

//*********************************************************************
//***************************** AUTH **********************************
//*********************************************************************

const signUpMutationFn = async (
  email: string,
  password: string,
  userData?: Record<string, unknown>
): Promise<{ user: User }> => {
  const payload = {
    email,
    password,
    metadata: userData
  }
  const response = await API.post('auth/signup', payload)
  return response.data
}
const getRefreshTokenQueryFn = async (
  currentRefreshToken: string
): Promise<{ access_token: string; refresh_token: string }> => {
  const response = await API.post(`/auth/refresh`, {
    refresh_token: currentRefreshToken
  })
  return response.data
}
const loginQueryFn = async (email: string, password: string) => {
  const resposne = await API.post('/auth/signin', { email, password })
  return resposne.data
}
const logoutQueryFn = async () => {
  const response = await API.get('auth/signout')
  return response.data
}

export {
  ingestionMutationFn,
  ingestionQueryFn,
  ingestionByIdQueryFn,
  ingestionTasksQueryFn,
  ingestionDeleteMutationFn,
  handleChatStream,
  sendMessage,
  embeddingDocumentByIdMutationFn,
  parseDocMutationFn,
  getParsersQueryFn,
  getParsingTasksQueryFn,
  getParsingTaskStatusByIdQueryFn,
  logoutQueryFn,
  loginQueryFn,
  getRefreshTokenQueryFn,
  signUpMutationFn
}
