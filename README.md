# 🌸 Nihongo Honeymoon App

A full-stack Japanese learning app built for a student with ADHD (combined type) preparing for a honeymoon trip to Osaka, Kyoto, Tokyo, and Kumamoto.

## Stack

| Layer    | Tech                        |
|----------|-----------------------------|
| Frontend | React 18 + Vite + Tailwind  |
| Backend  | FastAPI (Python)             |
| Database | MongoDB (via Motor + Beanie) |
| Auth     | JWT (python-jose + bcrypt)  |
| AI       | Anthropic Claude API         |
| Deploy   | Netlify (FE) + Railway (BE)  |

## Features

- ✅ **Task tracker** — ADHD-friendly daily task menu, 15 tasks, XP + streaks
- 🃏 **SRS Flashcards** — SM-2 spaced repetition with 20 seed cards, audio (Web Speech API), add your own
- 🤖 **AI Sensei** — Claude-powered Usui-sensei with 6 scenario modes (business intro, hotel, restaurant, taxi, emergency, free chat)
- 📊 **Dashboard** — Countdown to Japan, phase tracker, activity heatmap
- 📺 **Content library** — 12 curated items (anime, podcasts, drama, cooking, YouTube) filterable by city + type

---

## Local Setup

### 1. Clone & install

```bash
git clone <repo>

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values

# Frontend
cd ../frontend
npm install
```

### 2. Environment variables

**backend/.env**
```
MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net
MONGODB_DB=nihongo_app
SECRET_KEY=your-long-random-secret
ANTHROPIC_API_KEY=sk-ant-...
```

**frontend/.env**
```
VITE_API_URL=http://localhost:8000/api
```

### 3. Run locally

```bash
# Terminal 1 — backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

Visit `http://localhost:5173`

---

## Deployment

### Backend → Railway

1. Create a Railway project
2. Connect your GitHub repo
3. Set root directory to `/` (uses the Dockerfile)
4. Add environment variables in Railway dashboard
5. Deploy — note the public URL

### Frontend → Netlify

1. Connect your GitHub repo to Netlify
2. Build settings are in `netlify.toml`
3. Set environment variable: `VITE_API_URL=https://your-railway-url.railway.app/api`
4. Deploy

### MongoDB → MongoDB Atlas (free tier)

1. Create a free cluster at mongodb.com/atlas
2. Add a database user
3. Whitelist all IPs (`0.0.0.0/0`) for Railway
4. Copy the connection string to `MONGODB_URL`

---

## Architecture

```
frontend/
  src/
    pages/          # DashboardPage, TasksPage, FlashcardsPage, ChatPage, ContentPage
    components/ui/  # Layout, sidebar
    hooks/          # useAuth (Zustand store)
    lib/            # api.js (Axios client)

backend/
  main.py           # FastAPI app + CORS
  database.py       # MongoDB connection (Motor + Beanie)
  models/           # User, TaskLog, Flashcard, ProgressEntry, ContentItem
  routes/           # auth, tasks, flashcards, progress, chat, content
  services/
    auth_service.py # JWT, bcrypt
    srs_service.py  # SM-2 algorithm
```

---

## ADHD Design Principles

This app was designed specifically for **ADHD combined type**:

- **Max 15-min tasks** — no long sessions
- **Pick-any-3 daily menu** — removes decision paralysis
- **Movement tasks included** — walk & talk, bowing drill, kitchen vocab
- **XP + streaks** — dopamine-friendly progress feedback
- **6 AI scenarios** — short, varied, never repetitive
- **Hyperfocus-friendly** — deep content available when the spark hits
- **No guilt UX** — tasks can't be un-checked, but you can always come back

