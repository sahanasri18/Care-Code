import axios from 'axios'
import { authEpoch, bumpAuthEpoch, guardRefresh, StaleRefreshError } from './authSession'

const API_URL = import.meta.env.VITE_API_URL || ''
const PUBLIC_BASE = import.meta.env.VITE_PUBLIC_BASE_URL || ''

export const client = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

export const publicBase = PUBLIC_BASE || window.location.origin

export function absoluteUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `${publicBase}${path}`
}

const TOKEN_KEYS = {
  access: 'carecode_access',
  refresh: 'carecode_refresh',
}

export const tokenStore = {
  get access() {
    return localStorage.getItem(TOKEN_KEYS.access)
  },
  get refresh() {
    return localStorage.getItem(TOKEN_KEYS.refresh)
  },
  set(tokens) {
    localStorage.setItem(TOKEN_KEYS.access, tokens.access_token)
    localStorage.setItem(TOKEN_KEYS.refresh, tokens.refresh_token)
    bumpAuthEpoch()
  },
  clear() {
    localStorage.removeItem(TOKEN_KEYS.access)
    localStorage.removeItem(TOKEN_KEYS.refresh)
    bumpAuthEpoch()
  },
}

let refreshPromise = null

async function refreshTokens() {
  const refresh = tokenStore.refresh
  const epochAtStart = authEpoch()
  if (!refresh) throw new Error('no refresh token')
  const { data } = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
    refresh_token: refresh,
  })
  guardRefresh(epochAtStart)
  tokenStore.set(data)
  return data.access_token
}

client.interceptors.request.use((config) => {
  const token = tokenStore.access
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (
      error.response?.status === 401 &&
      !original._retried &&
      original.url !== '/api/v1/auth/login' &&
      original.url !== '/api/v1/auth/refresh'
    ) {
      original._retried = true
      try {
        refreshPromise = refreshPromise || refreshTokens()
        const newToken = await refreshPromise
        refreshPromise = null
        original.headers.Authorization = `Bearer ${newToken}`
        return client(original)
      } catch (e) {
        refreshPromise = null
        if (!(e instanceof StaleRefreshError)) {
          tokenStore.clear()
          window.dispatchEvent(new CustomEvent('carecode:logout'))
        }
      }
    }
    return Promise.reject(error)
  }
)

export function apiError(error, fallback = 'Something went wrong. Please try again.') {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join(', ')
  return fallback
}
