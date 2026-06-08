from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks, flashcards, progress, chat, content, auth
from database import connect_db, close_db

app = FastAPI(title="Nihongo App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(auth.router,       prefix="/api/auth",       tags=["auth"])
app.include_router(tasks.router,      prefix="/api/tasks",      tags=["tasks"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["flashcards"])
app.include_router(progress.router,   prefix="/api/progress",   tags=["progress"])
app.include_router(chat.router,       prefix="/api/chat",       tags=["chat"])
app.include_router(content.router,    prefix="/api/content",    tags=["content"])

@app.get("/")
async def root():
    return {"status": "ok", "app": "Nihongo Honeymoon App"}
