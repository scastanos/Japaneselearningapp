import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../hooks/useAuth'

export default function LoginPage() {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ email: '', password: '', name: '' })
  const [error, setError] = useState('')
  const { login, register, loading } = useAuthStore()
  const navigate = useNavigate()

  const handle = async e => {
    e.preventDefault()
    setError('')
    const result = mode === 'login'
      ? await login(form.email, form.password)
      : await register(form.email, form.password, form.name)
    if (result.ok) navigate('/')
    else setError(result.error)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sakura-light via-white to-matcha-light flex items-center justify-center p-4">
      <div className="card p-8 w-full max-w-sm">
        <div className="text-center mb-6">
          <h1 className="jp text-3xl font-bold text-sakura mb-1">日本語</h1>
          <p className="text-stone-500 text-sm">Honeymoon Japanese · 2026</p>
        </div>

        <form onSubmit={handle} className="flex flex-col gap-3">
          {mode === 'register' && (
            <input className="w-full border border-stone-200 rounded-xl px-3 py-2.5 text-sm outline-none focus:border-sakura"
              placeholder="Your name" value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} />
          )}
          <input type="email" className="w-full border border-stone-200 rounded-xl px-3 py-2.5 text-sm outline-none focus:border-sakura"
            placeholder="Email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required />
          <input type="password" className="w-full border border-stone-200 rounded-xl px-3 py-2.5 text-sm outline-none focus:border-sakura"
            placeholder="Password" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} required />
          {error && <p className="text-red-500 text-xs">{error}</p>}
          <button type="submit" disabled={loading} className="btn-primary w-full py-2.5 mt-1">
            {loading ? '...' : mode === 'login' ? 'Sign in' : 'Create account'}
          </button>
        </form>

        <p className="text-center text-xs text-stone-400 mt-4">
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button onClick={() => setMode(m => m === 'login' ? 'register' : 'login')}
            className="text-sakura hover:underline">
            {mode === 'login' ? 'Sign up' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  )
}
