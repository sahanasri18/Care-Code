import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { client, tokenStore } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const handleLogout = () => setUser(null)
    window.addEventListener('carecode:logout', handleLogout)
    return () => window.removeEventListener('carecode:logout', handleLogout)
  }, [])

  useEffect(() => {
    let mounted = true
    if (!tokenStore.access) {
      setLoading(false)
      return
    }
    client
      .get('/api/v1/users/me')
      .then((res) => {
        if (mounted) setUser(res.data)
      })
      .catch(() => {
        if (mounted) setUser(null)
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      isAdmin: Boolean(user?.role === 'admin'),
      login: async (email, password) => {
        const { data } = await client.post('/api/v1/auth/login', { email, password })
        tokenStore.set(data.tokens)
        setUser(data.user)
        return data.user
      },
      register: async (payload) => {
        const { data } = await client.post('/api/v1/auth/register', payload)
        tokenStore.set(data.tokens)
        setUser(data.user)
        return data.user
      },
      logout: async () => {
        try {
          await client.post('/api/v1/auth/logout', { refresh_token: tokenStore.refresh })
        } catch (e) {
          /* idempotent */
        }
        tokenStore.clear()
        setUser(null)
      },
    }),
    [user, loading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
