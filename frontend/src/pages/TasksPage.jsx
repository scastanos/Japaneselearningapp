import { useEffect, useState } from 'react'
import api from '../lib/api'
import { CheckCircle2, Circle, Zap } from 'lucide-react'
import clsx from 'clsx'

const TASKS = [
  { id:'anki-sprint',    name:'Anki sprint',       type:'anki',   duration:7,  color:'sakura', desc:'Due cards only. Stop when the timer fires, no guilt.' },
  { id:'shadow-drill',   name:'Shadowing drill',   type:'speak',  duration:10, color:'matcha', desc:'Pick 1 phrase from class. Repeat 10× with audio.' },
  { id:'travel-vlog',   name:'Japan travel vlog',  type:'watch',  duration:10, color:'ocean',  desc:'Watch with JP subtitles. Pause on words you recognize.' },
  { id:'mirror-speak',  name:'Speak to mirror',    type:'speak',  duration:5,  color:'sakura', desc:'All 3 introduction levels. Time yourself.' },
  { id:'teppei',        name:'Teppei podcast',     type:'listen', duration:10, color:'matcha', desc:'1 episode on a walk or commute. No notes needed.' },
  { id:'scenario',      name:'Honeymoon scenario', type:'speak',  duration:10, color:'yuzu',   desc:'Hotel, taxi, restaurant, or directions — pick one.' },
  { id:'city-vocab',    name:'City deep-dive',     type:'anki',   duration:10, color:'indigo', desc:'5 words about Osaka, Kyoto, Tokyo, or Kumamoto in JP.' },
  { id:'kana',          name:'Kana writing',       type:'write',  duration:7,  color:'indigo', desc:'Write 1 row of hiragana or katakana aloud.' },
  { id:'jp-text',       name:'Japanese texting',   type:'play',   duration:10, color:'ocean',  desc:'DM yourself or a partner class phrases in Japanese.' },
  { id:'bow-practice',  name:'Bowing practice',    type:'move',   duration:5,  color:'matcha', desc:'All 4 bow degrees + correct greeting for each.' },
  { id:'nhk-video',     name:'NHK World video',    type:'watch',  duration:15, color:'ocean',  desc:'Short Japan culture clip — NHK World app.' },
  { id:'menu-reading',  name:'Menu reading',       type:'play',   duration:10, color:'yuzu',   desc:'Find a real Kyoto/Osaka restaurant menu. Decode it.' },
  { id:'walk-talk',     name:'Walk & talk',        type:'move',   duration:10, color:'matcha', desc:'Say Japanese phrases aloud on a walk. No phone needed.' },
  { id:'kitchen-vocab', name:'Kitchen vocab',      type:'move',   duration:5,  color:'yuzu',   desc:'Label kitchen objects in Japanese. Say each as you touch it.' },
  { id:'tpr-roleplay',  name:'TPR role-play',      type:'move',   duration:15, color:'sakura', desc:'Physically act out: hotel check-in, meishi exchange, bowing.' },
]

const COLOR = {
  sakura: { bg:'bg-sakura-light', text:'text-sakura',  border:'border-sakura/30', dot:'bg-sakura' },
  matcha: { bg:'bg-matcha-light', text:'text-matcha',  border:'border-matcha/30', dot:'bg-matcha' },
  yuzu:   { bg:'bg-yuzu-light',   text:'text-yuzu',    border:'border-yuzu/30',   dot:'bg-yuzu' },
  indigo: { bg:'bg-indigo-light', text:'text-indigo',  border:'border-indigo/30', dot:'bg-indigo' },
  ocean:  { bg:'bg-ocean-light',  text:'text-ocean',   border:'border-ocean/30',  dot:'bg-ocean' },
}

export default function TasksPage() {
  const [completed, setCompleted] = useState(new Set())
  const [xpToday, setXpToday] = useState(0)
  const [celebrating, setCelebrating] = useState(null)

  useEffect(() => {
    api.get('/tasks/today').then(r => setCompleted(new Set(r.data.completed)))
  }, [])

  const toggle = async (task) => {
    if (completed.has(task.id)) return   // no un-completing
    try {
      const { data } = await api.post('/tasks/complete', {
        task_id: task.id, task_name: task.name,
        task_type: task.type, duration_minutes: task.duration
      })
      setCompleted(prev => new Set([...prev, task.id]))
      setXpToday(prev => prev + data.xp_earned)
      setCelebrating(task.id)
      setTimeout(() => setCelebrating(null), 1200)
    } catch (e) { console.error(e) }
  }

  const doneCount = completed.size

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h2 className="text-xl font-semibold text-stone-800">Daily task menu</h2>
          <p className="text-stone-400 text-sm mt-0.5">Pick any 3 tasks — variety is the point. Every type counts.</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-semibold text-stone-800">{doneCount}</div>
          <div className="text-xs text-stone-400">done today</div>
        </div>
      </div>

      {xpToday > 0 && (
        <div className="flex items-center gap-2 mb-4 bg-yuzu-light text-yuzu-dark px-4 py-2.5 rounded-xl text-sm font-medium">
          <Zap size={16} className="text-yuzu" />
          +{xpToday} XP earned today — great work!
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {TASKS.map(task => {
          const c = COLOR[task.color]
          const done = completed.has(task.id)
          const popping = celebrating === task.id
          return (
            <button key={task.id} onClick={() => toggle(task)}
              className={clsx(
                'text-left p-4 rounded-2xl border transition-all duration-200',
                done ? 'opacity-50 cursor-default' : 'hover:shadow-sm active:scale-[0.98] cursor-pointer',
                popping ? 'scale-105' : '',
                c.bg, c.border
              )}>
              <div className="flex items-start justify-between mb-2">
                <span className={clsx('text-xs font-semibold', c.text)}>
                  {task.duration} min · {task.type}
                </span>
                {done
                  ? <CheckCircle2 size={18} className={c.text} />
                  : <Circle size={18} className="text-stone-300" />
                }
              </div>
              <div className="font-semibold text-stone-800 text-sm mb-1">{task.name}</div>
              <div className="text-xs text-stone-500 leading-relaxed">{task.desc}</div>
            </button>
          )
        })}
      </div>

      {doneCount >= 3 && (
        <div className="mt-6 card p-4 text-center bg-matcha-light border-matcha/20">
          <p className="text-matcha font-medium">🎉 素晴らしい！You hit your daily goal!</p>
          <p className="text-sm text-stone-500 mt-1">Japan is getting closer every day.</p>
        </div>
      )}
    </div>
  )
}
