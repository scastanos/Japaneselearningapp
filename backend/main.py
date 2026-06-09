import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import ensure_db, ping_db
from routes import auth, chat, content, flashcards, progress, tasks

load_dotenv()


def allowed_origins() -> list[str]:
    raw = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:4173",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(title="NihonGo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def connect_database(request: Request, call_next):
    if request.url.path not in ("/", "/api/health"):
        try:
            await ensure_db()
        except Exception as exc:
            return JSONResponse(
                status_code=503,
                content={"detail": f"Database unavailable: {exc}"},
            )
    return await call_next(request)


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["flashcards"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(content.router, prefix="/api/content", tags=["content"])


@app.get("/")
async def root():
    return {"status": "ok", "app": "NihonGo"}


@app.get("/api/health")
async def health():
    try:
        db_ok = await ping_db()
        return {"status": "ok", "app": "NihonGo", "db": db_ok}
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "app": "NihonGo", "db": str(exc)},
        )
