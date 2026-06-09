import { Outlet, NavLink } from 'react-router-dom'
import { useAuthStore } from '../../hooks/useAuth'
import { LayoutDashboard, CheckSquare, BookOpen, MessageCircle, Play, LogOut, Flame } from 'lucide-react'

const nav = [
  { to: '/',          icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/tasks',     icon: CheckSquare,     label: 'Daily Tasks' },
  { to: '/flashcards',icon: BookOpen,        label: 'Flashcards' },
  { to: '/chat',      icon: MessageCircle,   label: 'AI Sensei' },
  { to: '/content',   icon: Play,            label: 'Watch & Listen' },
]

export default function Layout() {
  const { user, logout } = useAuthStore()

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-56 bg-white border-r border-stone-100 flex flex-col py-6 px-3 shrink-0">
        <div className="px-3 mb-6">
          <h1 className="text-lg font-semibold text-stone-900">
            <span className="jp text-sakura">日本語</span>
          </h1>
          <p className="text-xs text-stone-400 mt-0.5">NihonGo</p>
        </div>

        <nav className="flex flex-col gap-1 flex-1">
          {nav.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to} to={to} end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors
                 ${isActive ? 'bg-sakura-light text-sakura' : 'text-stone-500 hover:bg-stone-50 hover:text-stone-800'}`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        {user && (
          <div className="mt-auto px-3">
            <div className="flex items-center gap-2 mb-3 p-2 bg-yuzu-light rounded-xl">
              <Flame size={16} className="text-yuzu" />
              <span className="text-xs font-medium text-yuzu-dark">{user.streak_days} day streak</span>
              <span className="ml-auto text-xs text-stone-400">{user.xp} XP</span>
            </div>
            <button onClick={logout} className="flex items-center gap-2 text-xs text-stone-400 hover:text-stone-600 px-1">
              <LogOut size={14} /> Sign out
            </button>
          </div>
        )}
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-y-auto bg-stone-50 p-6">
        <Outlet />
      </main>
    </div>
  )
}
