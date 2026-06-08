from fastapi import APIRouter, Depends
from models.progress import ProgressEntry
from models.user import User
from services.auth_service import get_current_user
from datetime import datetime, date, timedelta

router = APIRouter()

def get_phase(study_date: str) -> int:
    d = date.fromisoformat(study_date)
    if d < date(2026, 7, 16): return 1
    if d < date(2026, 9, 8):  return 2
    if d < date(2026, 10, 20): return 3
    return 4

@router.get("/summary")
async def summary(user: User = Depends(get_current_user)):
    entries = await ProgressEntry.find(
        ProgressEntry.user_id == str(user.id)
    ).sort("-date").to_list()
    total_tasks = sum(e.tasks_completed for e in entries)
    total_cards = sum(e.cards_reviewed for e in entries)
    total_minutes = sum(e.minutes_studied for e in entries)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    current_phase = get_phase(today)

    # days until departure
    depart = date(2026, 11, 13)
    days_left = (depart - date.today()).days

    # last 14 days heatmap
    heatmap = []
    for i in range(13, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        match = next((e for e in entries if e.date == d), None)
        heatmap.append({"date": d, "tasks": match.tasks_completed if match else 0,
                         "xp": match.xp_earned if match else 0})
    return {
        "streak": user.streak_days,
        "xp": user.xp,
        "total_tasks": total_tasks,
        "total_cards": total_cards,
        "total_minutes": total_minutes,
        "current_phase": current_phase,
        "days_left": days_left,
        "heatmap": heatmap,
    }

@router.get("/history")
async def history(user: User = Depends(get_current_user)):
    entries = await ProgressEntry.find(
        ProgressEntry.user_id == str(user.id)
    ).sort("-date").limit(30).to_list()
    return [{"date": e.date, "tasks": e.tasks_completed,
             "cards": e.cards_reviewed, "minutes": e.minutes_studied,
             "xp": e.xp_earned} for e in entries]
