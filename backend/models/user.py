from beanie import Document
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
    email: EmailStr
    hashed_password: str
    name: str = "Student"
    created_at: datetime = datetime.utcnow()
    streak_days: int = 0
    last_study_date: Optional[str] = None   # "YYYY-MM-DD"
    xp: int = 0
    departure_date: str = "2026-11-13"

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str = "Student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    streak_days: int
    xp: int
    departure_date: str
