from beanie import Document
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class Flashcard(Document):
    user_id: str
    front: str              # Japanese (kanji/kana)
    front_reading: str      # hiragana reading
    back: str               # English meaning
    example: str = ""       # example sentence
    category: str = "general"   # general | business | travel | food | directions
    city: str = ""          # osaka | kyoto | tokyo | kumamoto | ""
    # SRS fields (SM-2 algorithm)
    ease_factor: float = 2.5
    interval: int = 1       # days until next review
    repetitions: int = 0
    next_review: str = ""   # "YYYY-MM-DD"
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "flashcards"

class FlashcardReview(Document):
    user_id: str
    card_id: str
    rating: int             # 0-5 (SM-2 scale)
    reviewed_at: datetime = datetime.utcnow()

    class Settings:
        name = "flashcard_reviews"

class FlashcardCreate(BaseModel):
    front: str
    front_reading: str
    back: str
    example: str = ""
    category: str = "general"
    city: str = ""

class ReviewSubmit(BaseModel):
    card_id: str
    rating: int             # 0=blackout, 1=wrong, 2=hard, 3=ok, 4=good, 5=easy
