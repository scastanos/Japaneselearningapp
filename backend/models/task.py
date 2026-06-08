from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskLog(Document):
    user_id: str
    task_id: str
    task_name: str
    task_type: str          # anki | speak | listen | watch | play | write | move
    duration_minutes: int
    date: str               # "YYYY-MM-DD"
    completed_at: datetime = datetime.utcnow()
    xp_earned: int = 10

    class Settings:
        name = "task_logs"

class TaskComplete(BaseModel):
    task_id: str
    task_name: str
    task_type: str
    duration_minutes: int = 10
