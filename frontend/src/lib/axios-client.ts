import { config } from '@/config/config'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
const baseURL = config.apiUrl

const options = {
  baseURL,
  withCredentials: true,
  timeout: 10000
}

const API = axios.create(options)
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const navigate = useNavigate()
    const originalRequest = error.config

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refreshToken')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/refresh`, {
          refresh_token: refreshToken
        })

        const { access_token, refresh_token: new_refresh_token } = response.data

        // Update tokens in localStorage
        localStorage.setItem('accessToken', access_token)
        localStorage.setItem('refreshToken', new_refresh_token)

        // Retry the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return API(originalRequest)
      } catch (refreshError) {
        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        navigate('/auth/login')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)
export { API }
