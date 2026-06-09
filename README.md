# NihonGo

Japanese learning app for preparing for a trip to Japan — built with ADHD-friendly design (short tasks, XP, streaks, and low-friction daily practice).

**Live:** Frontend on Netlify · Backend on Vercel · Database on MongoDB Atlas

## Stack

| Layer    | Tech                         |
|----------|------------------------------|
| Frontend | React 18 + Vite + Tailwind   |
| Backend  | FastAPI (Python)             |
| Database | MongoDB (Motor + Beanie)     |
| Auth     | JWT (python-jose + bcrypt)   |
| AI       | Anthropic Claude API         |
| Deploy   | Netlify (FE) + Vercel (BE)   |

## Features

- **Task tracker** — daily pick-any-3 menu, 15 tasks, XP + streaks
- **SRS flashcards** — SM-2 spaced repetition, seed cards, Web Speech audio
- **AI Sensei** — Claude-powered Usui-sensei with scenario modes (hotel, restaurant, taxi, emergency, free chat, and more)
- **Dashboard** — countdown to Japan, phase tracker, activity heatmap
- **Content library** — curated anime, podcasts, drama, and YouTube by city

---

## Local setup

```bash
git clone https://github.com/scastanos/Japaneselearningapp.git
cd Japaneselearningapp

# Backend
cd backend
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add MongoDB Atlas URL + keys

# Frontend
cd ../frontend
npm install
cp .env.example .env   # optional — defaults proxy to localhost:8000
```

**backend/.env**

```
MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=nihongo_app
SECRET_KEY=your-long-random-secret
ANTHROPIC_API_KEY=sk-ant-...
ALLOWED_ORIGINS=http://localhost:5173
```

**frontend/.env**

```
VITE_API_URL=http://localhost:8000/api
```

Run:

```bash
# Terminal 1
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

Open `http://localhost:5173`

---

## Deployment

### Backend → Vercel (git push)

1. Import the repo in [Vercel](https://vercel.com/new)
2. Leave **Root Directory** as `.` (`vercel.json` routes to `backend/main.py`)
3. Add environment variables in Vercel → Settings → Environment Variables:

   | Variable | Value |
   |----------|-------|
   | `MONGODB_URL` | Atlas connection string |
   | `MONGODB_DB` | `nihongo_app` |
   | `SECRET_KEY` | long random string |
   | `ANTHROPIC_API_KEY` | `sk-ant-...` |
   | `ALLOWED_ORIGINS` | `https://nihongoj.netlify.app,http://localhost:5173` |

4. Push to `main` — Vercel redeploys automatically
5. Verify: `https://your-project.vercel.app/api/health` → `{"status":"ok","db":true}`

**MongoDB Atlas:** Network Access must allow `0.0.0.0/0` (Vercel uses dynamic IPs). If your DB password has special characters (`@`, `#`, `/`, etc.), [URL-encode it](https://www.mongodb.com/docs/atlas/troubleshoot-connection/) in `MONGODB_URL`.

**Troubleshooting signup/login:** Visit `/api/health` on your Vercel URL. If `db` is not `true`, fix `MONGODB_URL` in Vercel and redeploy. If the browser blocks requests, add your Netlify URL to `ALLOWED_ORIGINS`.

### Frontend → Netlify (drag and drop)

Drag-and-drop cannot inject build-time env vars, so the API URL lives in `frontend/public/config.js`.

```bash
# Set your Vercel URL in frontend/public/config.js first
npm install --prefix frontend
npm run prepare:netlify
```

Drag **`netlify-drop/`** onto [app.netlify.com/drop](https://app.netlify.com/drop).

After deploy, add your Netlify URL to Vercel's `ALLOWED_ORIGINS` and redeploy the backend.

**Optional:** connect the repo to Netlify via Git — settings in `netlify.toml`.

---

## Project structure

```
frontend/
  src/pages/       Dashboard, Tasks, Flashcards, Chat, Content
  src/hooks/       useAuth (Zustand)
  src/lib/         api.js

backend/
  main.py          FastAPI app
  database.py      MongoDB (Motor + Beanie)
  routes/          auth, tasks, flashcards, progress, chat, content
  services/        auth, SRS (SM-2)
```

---

## ADHD design principles

- Max 15-minute tasks — no long sessions
- Pick-any-3 daily menu — reduces decision paralysis
- XP + streaks — progress feedback
- Short AI scenarios — varied, never repetitive
- No guilt UX — you can always come back
