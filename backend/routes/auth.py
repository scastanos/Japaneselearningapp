from fastapi import APIRouter, HTTPException
from models.user import User, UserCreate, UserLogin, UserOut
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register(data: UserCreate):
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        name=data.name
    )
    await user.insert()
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": UserOut(
        id=str(user.id), email=user.email, name=user.name,
        streak_days=0, xp=0, departure_date=user.departure_date
    )}

@router.post("/login")
async def login(data: UserLogin):
    user = await User.find_one(User.email == data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": UserOut(
        id=str(user.id), email=user.email, name=user.name,
        streak_days=user.streak_days, xp=user.xp, departure_date=user.departure_date
    )}

@router.get("/me")
async def me(user: User = __import__('fastapi').Depends(__import__('services.auth_service', fromlist=['get_current_user']).get_current_user)):
    return UserOut(
        id=str(user.id), email=user.email, name=user.name,
        streak_days=user.streak_days, xp=user.xp, departure_date=user.departure_date
    )
