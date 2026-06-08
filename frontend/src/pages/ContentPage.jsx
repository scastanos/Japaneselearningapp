import { useEffect, useState } from 'react'
import api from '../lib/api'
import { ExternalLink, Clock, Filter } from 'lucide-react'
import clsx from 'clsx'

const TYPE_EMOJI = { anime:'🎌', podcast:'🎧', drama:'📺', cooking:'🍳', shortStory:'📖', youtube:'▶️' }
const TYPE_LABEL = { anime:'Anime', podcast:'Podcast', drama:'Drama', cooking:'Cooking', shortStory:'Reading', youtube:'YouTube' }
const DIFF_COLOR = { beginner:'bg-matcha-light text-matcha', elementary:'bg-ocean-light text-ocean', intermediate:'bg-yuzu-light text-yuzu' }
const CITIES = ['','osaka','kyoto','tokyo','kumamoto']
const CITY_EMOJI = { osaka:'🏮', kyoto:'⛩️', tokyo:'🗼', kumamoto:'🏯' }

export default function ContentPage() {
  const [items, setItems]       = useState([])
  const [stats, setStats]       = useState(null)
  const [city, setCity]         = useState('')
  const [type, setType]         = useState('')
  const [difficulty, setDiff]   = useState('')
  const [types, setTypes]       = useState([])

  useEffect(() => {
    api.get('/content/types').then(r => setTypes(r.data))
    api.get('/content/stats').then(r => setStats(r.data))
  }, [])

  useEffect(() => {
    const params = {}
    if (city)       params.city = city
    if (type)       params.type = type
    if (difficulty) params.difficulty = difficulty
    api.get('/content/', { params }).then(r => setItems(r.data))
  }, [city, type, difficulty])

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-4 flex items-start justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-xl font-semibold text-stone-800">Watch & Listen</h2>
          <p className="text-stone-400 text-sm">{stats?.total || '...'} items curated for your trip · filter by city, type, or level</p>
        </div>
        {stats && (
          <div className="flex gap-3 text-xs text-stone-400 flex-wrap">
            {Object.entries(stats.by_type || {}).map(([t, n]) => (
              <span key={t}>{TYPE_EMOJI[t]} {n}</span>
            ))}
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="card p-3 mb-5 flex flex-col gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          <Filter size={13} className="text-stone-400"/>
          <span className="text-xs text-stone-400 font-medium w-10">City</span>
          {CITIES.map(c => (
            <button key={c} onClick={() => setCity(c)}
              className={clsx('text-xs px-2.5 py-1 rounded-full border transition-colors',
                city === c ? 'bg-sakura text-white border-sakura' : 'bg-white text-stone-500 border-stone-200 hover:border-stone-300')}>
              {c ? (CITY_EMOJI[c] + ' ' + c.charAt(0).toUpperCase() + c.slice(1)) : 'All cities'}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-stone-400 font-medium w-10">Type</span>
          <button onClick={() => setType('')}
            className={clsx('text-xs px-2.5 py-1 rounded-full border transition-colors',
              !type ? 'bg-ocean text-white border-ocean' : 'bg-white text-stone-500 border-stone-200 hover:border-stone-300')}>
            All types
          </button>
          {types.map(t => (
            <button key={t} onClick={() => setType(t)}
              className={clsx('text-xs px-2.5 py-1 rounded-full border transition-colors',
                type === t ? 'bg-ocean text-white border-ocean' : 'bg-white text-stone-500 border-stone-200 hover:border-stone-300')}>
              {TYPE_EMOJI[t]} {TYPE_LABEL[t] || t}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-stone-400 font-medium w-10">Level</span>
          {['','beginner','elementary','intermediate'].map(d => (
            <button key={d} onClick={() => setDiff(d)}
              className={clsx('text-xs px-2.5 py-1 rounded-full border transition-colors',
                difficulty === d ? 'bg-matcha text-white border-matcha' : 'bg-white text-stone-500 border-stone-200 hover:border-stone-300')}>
              {d || 'All levels'}
            </button>
          ))}
        </div>
      </div>

      <p className="text-xs text-stone-400 mb-3">{items.length} items shown</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item, i) => (
          <div key={i} className="card p-4 flex flex-col hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-2">
              <span className="text-2xl">{TYPE_EMOJI[item.type] || '📌'}</span>
              <div className="flex gap-1 flex-wrap justify-end">
                <span className={clsx('badge', DIFF_COLOR[item.difficulty] || 'bg-stone-100 text-stone-500')}>
                  {item.difficulty}
                </span>
                {item.city_tag && (
                  <span className="badge bg-stone-100 text-stone-500 capitalize">
                    {CITY_EMOJI[item.city_tag]} {item.city_tag}
                  </span>
                )}
              </div>
            </div>
            <h3 className="font-semibold text-stone-800 text-sm mb-1.5 leading-snug">{item.title}</h3>
            <p className="text-xs text-stone-500 leading-relaxed mb-3 flex-1">{item.description}</p>
            <div className="flex items-center justify-between mt-auto pt-2 border-t border-stone-50">
              <span className="flex items-center gap-1 text-xs text-stone-400">
                <Clock size={11}/> {item.duration_minutes} min
              </span>
              <a href={item.url} target="_blank" rel="noopener noreferrer"
                className="flex items-center gap-1 text-xs text-sakura hover:text-sakura-dark font-medium transition-colors">
                Open <ExternalLink size={11}/>
              </a>
            </div>
            {item.tags?.length > 0 && (
              <div className="flex gap-1 flex-wrap mt-2">
                {item.tags.slice(0,4).map(t => (
                  <span key={t} className="text-xs bg-stone-50 text-stone-400 px-2 py-0.5 rounded-full">#{t}</span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {items.length === 0 && (
        <div className="text-center py-12 text-stone-400">
          <p className="text-4xl mb-3">🔍</p>
          <p>No content matches those filters. Try removing one.</p>
        </div>
      )}
    </div>
  )
}
