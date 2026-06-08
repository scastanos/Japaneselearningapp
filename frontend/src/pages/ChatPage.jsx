import { useState, useRef, useEffect } from 'react'
import api from '../lib/api'
import { Send, Bot, User, RefreshCw } from 'lucide-react'
import clsx from 'clsx'

const STARTERS = {
  general:    "こんにちは！I'm Usui-sensei 🌸 What would you like to practice today?\n\nType **scenarios** to see all 13 practice modes, or just start chatting!",
  business:   "はじめまして！Let's practice business introductions.\n\nI'll go first:\n【Usui-sensei】はじめまして。臼井江美と申します。昭和ボストンで日本語を教えております。どうぞよろしくお願いいたします。\n\nYour turn — try Level 1 (Polite) first!",
  hotel:      "Welcome to Kyoto! 🏯 You've just arrived at a beautiful ryokan.\n\nStaff: いらっしゃいませ！\n\nTry saying: チェックインをお願いします。\n(chekku in wo onegaishimasu)",
  restaurant: "You're at an izakaya in Osaka near Dotonbori! 🍺\n\nThe server is approaching. Start by getting their attention!\n\nTry: すみません！\n(sumimasen)",
  taxi:       "You're outside Kumamoto Station 🚕\n\nA taxi pulls up. The driver opens the window.\n\nTry telling him where you want to go:\n熊本城まで、お願いします！\n(Kumamotojou made, onegaishimasu)",
  onsen:      "Welcome to Kurokawa Onsen ♨️ One of Japan's most beautiful hot spring towns!\n\nLet's start with the most important phrase:\n【温泉に入りたいです】(onsen ni hairitai desu) = I want to take a hot spring bath\n\nShall we practice booking a 貸切風呂 (private bath)?",
  shopping:   "You're in Shinsaibashi, Osaka's famous shopping street 🛍️\n\nYou spot a beautiful omiyage shop. Step inside!\n\nTry: 見てもいいですか？\n(mite mo ii desu ka — May I look?)",
  shrine:     "You're at Fushimi Inari Shrine in Kyoto ⛩️ The famous torii gate tunnel!\n\nFirst things first — let's learn the proper visiting sequence. Step 1 is 手水 (temizu) — purifying your hands.\n\nReady to learn all 5 steps?",
  emergency:  "Let's cover emergency phrases 🆘 I hope you never need these, but knowing them brings real peace of mind.\n\nThe most important one first:\n【助けてください！】(tasukete kudasai!) = Please help me!\n\nSay it back to me — go!",
  shinkansen: "Shinkansen time! 🚅 You're at Shin-Osaka Station heading to Tokyo.\n\nFirst phrase:\n【新幹線の切符をください】(shinkansen no kippu wo kudasai) = A shinkansen ticket please\n\nNow — where do you want to go?",
  konbini:    "You're at a 7-Eleven in Tokyo at midnight 🏪 (Very authentic Japan experience!)\n\nThe staff will say: いらっしゃいませ！\nYou pick up an onigiri and want it heated.\n\nTry: 温めてください。\n(atatamete kudasai — please heat this)",
  kansai:     "Kansai-ben time! 😄 Learning even a few Osaka dialect phrases will absolutely delight locals.\n\nLesson 1: Instead of ありがとう (arigato), say:\n【おおきに】(ookini) = Thank you (Osaka!)\n\nSay it! Then I'll teach you めっちゃ next 🎉",
  honeymoon:  "Congratulations on getting married! 💑🌸\n\nThe most important honeymoon phrase:\n【新婚旅行で来ました】(shinkon ryokou de kimashita) = We came on our honeymoon!\n\nJapanese people LOVE this — you'll get wonderful reactions. Try saying it!",
}

export default function ChatPage() {
  const [scenarios, setScenarios] = useState([])
  const [scenario, setScenario] = useState('general')
  const [messages, setMessages] = useState([{ role:'assistant', content: STARTERS['general'] }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef()

  useEffect(() => {
    api.get('/chat/scenarios').then(r => setScenarios(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior:'smooth' })
  }, [messages])

  const changeScenario = (s) => {
    setScenario(s)
    setMessages([{ role:'assistant', content: STARTERS[s] || STARTERS['general'] }])
    setInput('')
  }

  const send = async () => {
    if (!input.trim() || loading) return
    const userMsg = { role:'user', content: input.trim() }
    const newMsgs = [...messages, userMsg]
    setMessages(newMsgs)
    setInput('')
    setLoading(true)
    try {
      const { data } = await api.post('/chat/message', { messages: newMsgs, scenario })
      setMessages(m => [...m, { role:'assistant', content: data.reply }])
    } catch {
      setMessages(m => [...m, { role:'assistant', content:'⚠️ Connection error. Check your API key in backend/.env' }])
    } finally { setLoading(false) }
  }

  return (
    <div className="max-w-2xl mx-auto flex flex-col" style={{ height:'calc(100vh - 48px)' }}>
      <div className="mb-3">
        <h2 className="text-xl font-semibold text-stone-800">AI Sensei — 臼井先生</h2>
        <p className="text-stone-400 text-sm">13 scenario modes · powered by Claude · short sessions, high variety</p>
      </div>

      {/* Scenario grid */}
      <div className="grid grid-cols-3 sm:grid-cols-4 gap-1.5 mb-3">
        {scenarios.map(s => (
          <button key={s.id} onClick={() => changeScenario(s.id)} title={s.desc}
            className={clsx('text-xs px-2 py-1.5 rounded-lg border transition-colors text-left leading-tight',
              scenario === s.id
                ? 'bg-sakura text-white border-sakura'
                : 'bg-white text-stone-600 border-stone-200 hover:border-stone-300')}>
            {s.label}
          </button>
        ))}
        <button onClick={() => changeScenario(scenario)} title="Restart this scenario"
          className="text-xs px-2 py-1.5 rounded-lg border border-stone-200 bg-white text-stone-400 hover:text-stone-600 flex items-center gap-1">
          <RefreshCw size={10}/> restart
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto card p-4 mb-3 flex flex-col gap-4">
        {messages.map((m, i) => (
          <div key={i} className={clsx('flex gap-3', m.role === 'user' && 'flex-row-reverse')}>
            <div className={clsx('w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5',
              m.role === 'assistant' ? 'bg-sakura-light' : 'bg-stone-100')}>
              {m.role === 'assistant'
                ? <Bot size={14} className="text-sakura"/>
                : <User size={14} className="text-stone-400"/>}
            </div>
            <div className={clsx('max-w-[82%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap',
              m.role === 'assistant'
                ? 'bg-white border border-stone-100 text-stone-700'
                : 'bg-sakura text-white')}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div className="w-7 h-7 rounded-full bg-sakura-light flex items-center justify-center">
              <Bot size={14} className="text-sakura"/>
            </div>
            <div className="bg-white border border-stone-100 rounded-2xl px-4 py-3 text-sm text-stone-400 italic">
              先生 is thinking…
            </div>
          </div>
        )}
        <div ref={bottomRef}/>
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input className="flex-1 border border-stone-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-sakura"
          placeholder="Type in English or Japanese…"
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}/>
        <button onClick={send} disabled={loading || !input.trim()}
          className="btn-primary px-4 disabled:opacity-40">
          <Send size={15}/>
        </button>
      </div>
    </div>
  )
}
