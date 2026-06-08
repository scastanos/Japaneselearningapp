from beanie import Document
from typing import List

class ContentItem(Document):
    title: str
    type: str
    url: str
    description: str
    difficulty: str = "beginner"
    duration_minutes: int = 10
    city_tag: str = ""
    tags: List[str] = []
    thumbnail: str = ""

    class Settings:
        name = "content"
