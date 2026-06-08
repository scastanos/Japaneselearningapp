from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProgressEntry(Document):
    user_id: str
    date: str               # "YYYY-MM-DD"
    tasks_completed: int = 0
    cards_reviewed: int = 0
    minutes_studied: int = 0
    xp_earned: int = 0
    phase: int = 1          # 1-4

    class Settings:
        name = "progress"

class ContentItem(Document):
    title: str
    type: str               # anime | podcast | drama | cooking | shortStory | youtube
    url: str
    description: str
    difficulty: str         # beginner | elementary | intermediate
    duration_minutes: int = 10
    city_tag: str = ""
    tags: List[str] = []
    thumbnail: str = ""

    class Settings:
        name = "content"
