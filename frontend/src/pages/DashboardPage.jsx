import { useEffect, useState } from 'react'
import { useAuthStore } from '../hooks/useAuth'
import { differenceInDays, parseISO } from 'date-fns'
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import api from '../lib/api'
import { Flame, Star, BookOpen, Clock, Plane } from 'lucide-react'

const PHASES = [
  { num: 1, label: 'Foundation & Course', dates: 'Jun 6 – Jul 15', color: 'bg-sakura-light text-sakura' },
  { num: 2, label: 'Consolidation',       dates: 'Jul 16 – Sep 7', color: 'bg-matcha-light text-matcha' },
  { num: 3, label: 'Active Immersion',    dates: 'Sep 8 – Oct 19', color: 'bg-yuzu-light text-yuzu' },
  { num: 4, label: 'Final Polish',        dates: 'Oct 20 – Nov 12', color: 'bg-indigo-light text-indigo' },
]

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    api.get('/progress/summary').then(r => setSummary(r.data))
  }, [])

  const daysLeft = user ? differenceInDays(new Date('2026-11-13'), new Date()) : 0
  const phase = summary?.current_phase || 1

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-stone-800">
          おはようございます, {user?.name} <span className="jp">🌸</span>
        </h2>
        <p className="text-stone-400 text-sm mt-0.5">Keep going — Japan is {daysLeft} days away</p>
      </div>

      {/* Countdown + stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { icon: Plane,    label: 'Days to Japan', value: daysLeft,                   color: 'text-sakura' },
          { icon: Flame,    label: 'Day streak',    value: user?.streak_days || 0,      color: 'text-yuzu' },
          { icon: Star,     label: 'Total XP',      value: user?.xp || 0,              color: 'text-indigo' },
          { icon: BookOpen, label: 'Cards reviewed', value: summary?.total_cards || 0,  color: 'text-matcha' },
        ].map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="card p-4">
            <Icon size={18} className={`${color} mb-2`} />
            <div className="text-2xl font-semibold text-stone-800">{value}</div>
            <div className="text-xs text-stone-400 mt-0.5">{label}</div>
          </div>
        ))}
      </div>

      {/* Phase indicator */}
      <div className="card p-4 mb-6">
        <p className="text-xs font-medium text-stone-400 uppercase tracking-wider mb-3">Study phases</p>
        <div className="flex gap-2 flex-wrap">
          {PHASES.map(p => (
            <div key={p.num}
              className={`flex-1 min-w-[120px] rounded-xl p-3 border-2 transition-all
                ${p.num === phase ? p.color + ' border-current' : 'bg-stone-50 text-stone-400 border-transparent'}`}>
              <div className="text-xs font-semibold mb-0.5">Phase {p.num}</div>
              <div className="text-xs font-medium leading-tight">{p.label}</div>
              <div className="text-xs opacity-70 mt-1">{p.dates}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Activity heatmap */}
      {summary?.heatmap && (
        <div className="card p-4 mb-6">
          <p className="text-xs font-medium text-stone-400 uppercase tracking-wider mb-3">Last 14 days</p>
          <ResponsiveContainer width="100%" height={80}>
            <BarChart data={summary.heatmap} barSize={16}>
              <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={d => d.slice(5)} />
              <Tooltip formatter={(v) => [`${v} tasks`, '']} labelFormatter={l => l} />
              <Bar dataKey="tasks" radius={[4,4,0,0]}>
                {summary.heatmap.map((entry, i) => (
                  <Cell key={i} fill={entry.tasks > 0 ? '#D4537E' : '#f5f5f4'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Destinations */}
      <div className="card p-4">
        <p className="text-xs font-medium text-stone-400 uppercase tracking-wider mb-3">Japan destinations</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {[
            { city: '大阪', en: 'Osaka',    emoji: '🏮', tip: 'たこ焼き (takoyaki) awaits' },
            { city: '京都', en: 'Kyoto',    emoji: '⛩️', tip: 'Fushimi Inari & ryokan' },
            { city: '東京', en: 'Tokyo',    emoji: '🗼', tip: 'JR trains & Shibuya' },
            { city: '熊本', en: 'Kumamoto', emoji: '🏯', tip: 'Kumamoto Castle' },
          ].map(d => (
            <div key={d.en} className="bg-stone-50 rounded-xl p-3 text-center">
              <div className="text-xl mb-1">{d.emoji}</div>
              <div className="jp font-bold text-stone-800 text-sm">{d.city}</div>
              <div className="text-xs text-stone-400">{d.en}</div>
              <div className="text-xs text-stone-400 mt-1">{d.tip}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
