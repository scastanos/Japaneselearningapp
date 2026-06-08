from fastapi import APIRouter, Depends
from models.task import TaskLog, TaskComplete
from models.user import User
from models.progress import ProgressEntry
from services.auth_service import get_current_user
from datetime import datetime

router = APIRouter()

XP_MAP = {"anki": 15, "speak": 20, "listen": 10, "watch": 10, "play": 15, "write": 15, "move": 20}

@router.post("/complete")
async def complete_task(data: TaskComplete, user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    xp = XP_MAP.get(data.task_type, 10)

    log = TaskLog(
        user_id=str(user.id),
        task_id=data.task_id,
        task_name=data.task_name,
        task_type=data.task_type,
        duration_minutes=data.duration_minutes,
        date=today,
        xp_earned=xp
    )
    await log.insert()

    # update or create today's progress entry
    entry = await ProgressEntry.find_one(
        ProgressEntry.user_id == str(user.id),
        ProgressEntry.date == today
    )
    if entry:
        entry.tasks_completed += 1
        entry.minutes_studied += data.duration_minutes
        entry.xp_earned += xp
        await entry.save()
    else:
        await ProgressEntry(
            user_id=str(user.id), date=today,
            tasks_completed=1, minutes_studied=data.duration_minutes, xp_earned=xp
        ).insert()

    # update streak
    user.xp += xp
    last = user.last_study_date
    if last != today:
        from datetime import date, timedelta
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        if last == yesterday:
            user.streak_days += 1
        elif last != today:
            user.streak_days = 1
        user.last_study_date = today
    await user.save()

    return {"xp_earned": xp, "total_xp": user.xp, "streak": user.streak_days}

@router.get("/today")
async def today_tasks(user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    logs = await TaskLog.find(
        TaskLog.user_id == str(user.id),
        TaskLog.date == today
    ).to_list()
    return {"completed": [l.task_id for l in logs], "count": len(logs)}
