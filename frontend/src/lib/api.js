import axios from 'axios'

function resolveApiBase() {
  if (typeof window !== 'undefined' && window.__NIHON_API_URL__) {
    return window.__NIHON_API_URL__.replace(/\/$/, '')
  }

  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL.replace(/\/$/, '')
  }

  return '/api'
}

const api = axios.create({
  baseURL: resolveApiBase(),
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
