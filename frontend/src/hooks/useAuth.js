import { create } from 'zustand'
import api from '../lib/api'

export const useAuthStore = create((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  loading: false,

  login: async (email, password) => {
    set({ loading: true })
    try {
      const { data } = await api.post('/auth/login', { email, password })
      localStorage.setItem('token', data.access_token)
      set({ token: data.access_token, user: data.user, loading: false })
      return { ok: true }
    } catch (e) {
      set({ loading: false })
      const detail = e.response?.data?.detail
      const message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail[0]?.msg : null
      return { ok: false, error: message || 'Login failed — check API connection' }
    }
  },

  register: async (email, password, name) => {
    set({ loading: true })
    try {
      const { data } = await api.post('/auth/register', { email, password, name })
      localStorage.setItem('token', data.access_token)
      set({ token: data.access_token, user: data.user, loading: false })
      return { ok: true }
    } catch (e) {
      set({ loading: false })
      const detail = e.response?.data?.detail
      const message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail[0]?.msg : null
      return { ok: false, error: message || 'Registration failed — check API connection' }
    }
  },

  fetchMe: async () => {
    const token = get().token
    if (!token) return
    try {
      const { data } = await api.get('/auth/me')
      set({ user: data })
    } catch { get().logout() }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  }
}))
