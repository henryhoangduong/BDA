import { config } from '@/config/config'
import axios from 'axios'

const baseURL = config.apiUrl

const options = {
  baseURL,
  withCredentials: true,
  timeout: 10000
}

export const API = axios.create(options)
