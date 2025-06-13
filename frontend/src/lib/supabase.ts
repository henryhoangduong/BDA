import { AuthResponse, SignInCredentials, SignUpCredentials, User } from '@/types/auth'
import { loginQueryFn, signUpMutationFn } from './api'
import { getRefreshTokenQueryFn } from './api'
const handleAuthError = async () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('userId')
  localStorage.removeItem('userEmail')
  if (typeof window !== 'undefined') {
    console.error('Authentication error, redirecting to login.')
    window.location.href = '/auth/login'
  } else {
    console.error('Authentication error occurred in non-browser environment.')
  }
}

const signUp = async ({
  email,
  password,
  userData
}: {
  email: string
  password: string
  userData?: Record<string, unknown>
}): Promise<User> => {
  try {
    const response = await signUpMutationFn(email, password, userData)

    if (response && response.user) {
      localStorage.setItem('userId', response.user.id)
      localStorage.setItem('userEmail', response.user.email)
    }

    return response.user
  } catch (error: unknown) {
    let errorMessage = 'Failed to sign up'
    if (error instanceof Error) {
      errorMessage = error.message
    }
    throw new Error(errorMessage)
  }
}
const getAccessToken = (): string | null => {
  return localStorage.getItem('accessToken')
}
const isAuthenticated = (): boolean => {
  return !!getAccessToken()
}
const refreshToken = async () => {
  const currentRefreshToken = localStorage.getItem('refreshToken')
  if (!currentRefreshToken) {
    throw new Error('No refresh token available')
  }
  try {
    const response = await getRefreshTokenQueryFn(currentRefreshToken)

    const { access_token, refresh_token: new_refresh_token } = response

    if (!access_token || !new_refresh_token) {
      throw new Error('Invalid token refresh response')
    }

    localStorage.setItem('accessToken', access_token)
    localStorage.setItem('refreshToken', new_refresh_token)

    return access_token
  } catch (error: unknown) {
    let errorMessage = 'Failed to refresh token'
    if (error instanceof Error) {
      errorMessage = error.message
    }
    throw new Error(errorMessage)
  }
}
const signIn = async (email: string, password: string): Promise<AuthResponse> => {
  try {
    const response = await loginQueryFn(email, password)
    const data = response

    // Make sure we have a valid session structure
    if (!data || !data.session || !data.user) {
      throw new Error('Invalid authentication response from server')
    }

    // Store tokens in localStorage
    localStorage.setItem('accessToken', data.session.access_token)
    localStorage.setItem('refreshToken', data.session.refresh_token)

    // Also store user information
    localStorage.setItem('userId', data.user.id)
    localStorage.setItem('userEmail', data.user.email)

    return data
  } catch (error: unknown) {
    let errorMessage = 'Failed to sign in'
    if (error instanceof Error) {
      errorMessage = error.message
    }
    throw new Error(errorMessage)
  }
}
const resetPassword = (email: string) => {
  return
}
const signOut = async (): Promise<void> => {
  try {
    // await httpClient.post(`/auth/signout`)
  } finally {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userId')
    localStorage.removeItem('userEmail')
  }
}
export { handleAuthError, signUp, getAccessToken, isAuthenticated, refreshToken, signIn, resetPassword, signOut }
