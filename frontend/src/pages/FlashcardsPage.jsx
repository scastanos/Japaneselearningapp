import { useEffect, useState } from 'react'
import api from '../lib/api'
import { RotateCcw, Volume2, Plus } from 'lucide-react'
import clsx from 'clsx'

const RATINGS = [
  { value: 1, label: '✗ Blank',  color: 'bg-red-100 text-red-700 hover:bg-red-200' },
  { value: 2, label: '~ Hard',   color: 'bg-orange-100 text-orange-700 hover:bg-orange-200' },
  { value: 3, label: '○ OK',     color: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' },
  { value: 4, label: '◎ Good',   color: 'bg-green-100 text-green-700 hover:bg-green-200' },
  { value: 5, label: '★ Easy',   color: 'bg-matcha-light text-matcha hover:bg-green-100' },
]

export default function FlashcardsPage() {
  const [cards, setCards] = useState([])
  const [idx, setIdx] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [done, setDone] = useState(false)
  const [reviewed, setReviewed] = useState(0)
  const [mode, setMode] = useState('review')  // review | add | browse
  const [addForm, setAddForm] = useState({ front:'', front_reading:'', back:'', example:'', category:'general', city:'' })

  const load = async () => {
    await api.post('/flashcards/seed').catch(() => {})
    const { data } = await api.get('/flashcards/due')
    setCards(data)
    setIdx(0)
    setFlipped(false)
    setDone(data.length === 0)
  }
  useEffect(() => { load() }, [])

  const current = cards[idx]

  const rate = async (rating) => {
    if (!current) return
    await api.post('/flashcards/review', { card_id: current.id, rating })
    setReviewed(r => r + 1)
    const next = idx + 1
    if (next >= cards.length) setDone(true)
    else { setIdx(next); setFlipped(false) }
  }

  const speak = (text) => {
    const u = new SpeechSynthesisUtterance(text)
    u.lang = 'ja-JP'
    speechSynthesis.speak(u)
  }

  const addCard = async (e) => {
    e.preventDefault()
    await api.post('/flashcards/add', addForm)
    setAddForm({ front:'', front_reading:'', back:'', example:'', category:'general', city:'' })
    setMode('review')
    load()
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-stone-800">Flashcards</h2>
          <p className="text-stone-400 text-sm">SM-2 spaced repetition · {cards.length} cards due</p>
        </div>
        <div className="flex gap-2">
          {['review','add','browse'].map(m => (
            <button key={m} onClick={() => setMode(m)}
              className={clsx('btn-secondary capitalize text-xs px-3 py-1.5', mode === m && 'bg-sakura-light text-sakura')}>
              {m === 'add' ? <><Plus size={12} className="inline mr-1"/>Add</> : m}
            </button>
          ))}
        </div>
      </div>

      {mode === 'review' && (
        done ? (
          <div className="card p-8 text-center">
            <div className="text-4xl mb-3">🎉</div>
            <h3 className="font-semibold text-stone-800 mb-1">All done for today!</h3>
            <p className="text-stone-400 text-sm mb-4">You reviewed {reviewed} cards. Come back tomorrow.</p>
            <button onClick={load} className="btn-secondary"><RotateCcw size={14} className="inline mr-1"/>Refresh</button>
          </div>
        ) : current ? (
          <div>
            <div className="text-xs text-stone-400 mb-3 text-right">{idx + 1} / {cards.length}</div>
            <div className="card p-8 cursor-pointer select-none mb-4" onClick={() => setFlipped(f => !f)}
              style={{ minHeight: 220 }}>
              <div className="text-center">
                <div className="badge mb-3 bg-stone-100 text-stone-500">{current.category} {current.city && `· ${current.city}`}</div>
                <div className="jp text-4xl font-bold text-stone-800 mb-2">{current.front}</div>
                <div className="text-stone-400 text-sm mb-4">{current.front_reading}</div>
                <button onClick={e => { e.stopPropagation(); speak(current.front) }}
                  className="text-stone-300 hover:text-sakura transition-colors">
                  <Volume2 size={20} />
                </button>
                {flipped && (
                  <div className="mt-6 pt-6 border-t border-stone-100">
                    <div className="text-xl font-semibold text-stone-800 mb-2">{current.back}</div>
                    {current.example && (
                      <div className="jp text-sm text-stone-500 italic">{current.example}</div>
                    )}
                  </div>
                )}
                {!flipped && <p className="text-xs text-stone-300 mt-6">Tap to reveal</p>}
              </div>
            </div>
            {flipped && (
              <div className="grid grid-cols-5 gap-2">
                {RATINGS.map(r => (
                  <button key={r.value} onClick={() => rate(r.value)}
                    className={clsx('py-2 px-1 rounded-xl text-xs font-medium transition-colors', r.color)}>
                    {r.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        ) : null
      )}

      {mode === 'add' && (
        <div className="card p-6">
          <h3 className="font-semibold text-stone-800 mb-4">Add a card</h3>
          <form onSubmit={addCard} className="flex flex-col gap-3">
            {[
              { key:'front', label:'Japanese (kanji/kana)', ph:'はじめまして' },
              { key:'front_reading', label:'Reading (romaji/hiragana)', ph:'hajimemashite' },
              { key:'back', label:'English meaning', ph:'Nice to meet you' },
              { key:'example', label:'Example sentence (optional)', ph:'はじめまして、スミスです。' },
            ].map(f => (
              <div key={f.key}>
                <label className="text-xs text-stone-500 mb-1 block">{f.label}</label>
                <input className="w-full border border-stone-200 rounded-xl px-3 py-2 text-sm outline-none focus:border-sakura"
                  placeholder={f.ph} value={addForm[f.key]}
                  onChange={e => setAddForm(p => ({ ...p, [f.key]: e.target.value }))}
                  required={f.key !== 'example'} />
              </div>
            ))}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-stone-500 mb-1 block">Category</label>
                <select className="w-full border border-stone-200 rounded-xl px-3 py-2 text-sm outline-none focus:border-sakura"
                  value={addForm.category} onChange={e => setAddForm(p => ({ ...p, category: e.target.value }))}>
                  {['general','business','travel','food','directions'].map(c => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-stone-500 mb-1 block">City (optional)</label>
                <select className="w-full border border-stone-200 rounded-xl px-3 py-2 text-sm outline-none focus:border-sakura"
                  value={addForm.city} onChange={e => setAddForm(p => ({ ...p, city: e.target.value }))}>
                  <option value="">—</option>
                  {['osaka','kyoto','tokyo','kumamoto'].map(c => <option key={c}>{c}</option>)}
                </select>
              </div>
            </div>
            <button type="submit" className="btn-primary mt-1">Add card</button>
          </form>
        </div>
      )}

      {mode === 'browse' && <BrowseCards />}
    </div>
  )
}

function BrowseCards() {
  const [cards, setCards] = useState([])
  const [filter, setFilter] = useState('')
  useEffect(() => { api.get('/flashcards/all').then(r => setCards(r.data)) }, [])
  const filtered = filter ? cards.filter(c => c.category === filter || c.city === filter) : cards
  return (
    <div>
      <div className="flex gap-2 mb-4 flex-wrap">
        {['','general','business','travel','food','directions','osaka','kyoto','tokyo','kumamoto'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={clsx('text-xs px-3 py-1 rounded-full border transition-colors',
              filter === f ? 'bg-sakura text-white border-sakura' : 'bg-white text-stone-500 border-stone-200 hover:border-stone-300')}>
            {f || 'All'}
          </button>
        ))}
      </div>
      <div className="flex flex-col gap-2">
        {filtered.map(c => (
          <div key={c.id} className="card p-3 flex items-center justify-between">
            <div>
              <span className="jp font-bold text-stone-800 mr-2">{c.front}</span>
              <span className="text-stone-400 text-sm">{c.back}</span>
            </div>
            <div className="text-xs text-stone-300">next: {c.next_review}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
