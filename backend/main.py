import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import close_db, connect_db
from routes import auth, chat, content, flashcards, progress, tasks

load_dotenv()


def allowed_origins() -> list[str]:
    raw = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:4173",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="Nihongo App API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["flashcards"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(content.router, prefix="/api/content", tags=["content"])


@app.get("/")
async def root():
    return {"status": "ok", "app": "Nihongo Honeymoon App"}


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "Nihongo Honeymoon App"}
