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
      return { ok: false, error: e.response?.data?.detail || 'Login failed' }
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
      return { ok: false, error: e.response?.data?.detail || 'Registration failed' }
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
