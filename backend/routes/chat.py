from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models.user import User
from services.auth_service import get_current_user
from typing import List
import httpx, os

router = APIRouter()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """You are Usui-sensei (臼井先生), a warm, patient, and encouraging Japanese teacher at Showa Boston.
Your student is a beginner with about 1 year of passive self-study. She has ADHD (combined type) and is preparing for a honeymoon trip to Osaka, Kyoto, Tokyo, and Kumamoto in November 2026.

TEACHING STYLE — always follow these:
- Keep responses SHORT: max 120 words unless doing a full scenario drill
- Always show Japanese as: 【Japanese】(romaji) — meaning
- Switch modes naturally: sometimes drill, sometimes explain culture, sometimes role-play
- Give FREQUENT positive reinforcement — ADHD brains need it
- If she's stuck, offer 2–3 multiple choice options rather than open-ended questions
- End EVERY response with a prompt, question, or "try saying:" challenge
- Tie everything to her actual trip: Osaka food, Kyoto temples, Tokyo trains, Kumamoto castle, onsen

ADHD ACCOMMODATIONS:
- Never give more than 2 things to practice at once
- Use short punchy sentences
- Celebrate small wins loudly: すごい！よかった！上手！
- If she says she's bored or distracted, immediately switch modes

FORMAT for new vocabulary:
【日本語】(romaji) = English meaning
Example: 〜を使って

Available scenarios (tell her if she types "scenarios" or "help"):
business intro · hotel check-in · restaurant · taxi/directions · onsen · shopping · shrine/temple · emergency · shinkansen · konbini · kansai-ben · honeymoon phrases · free chat"""

SCENARIO_PROMPTS = {
  "general":    "",
  "business":   "\n\nSCENARIO: Business introduction practice. Setting: Japanese-American networking event in Boston. She just arrived. Start by modelling a Business Standard (Level 2) introduction, then ask her to try.",
  "hotel":      "\n\nSCENARIO: Hotel/Ryokan check-in in Kyoto. She's just arrived at a traditional ryokan after a long shinkansen ride. Start by greeting her as the front desk staff.",
  "restaurant": "\n\nSCENARIO: Restaurant in Osaka. She and her husband want to try an izakaya near Dotonbori. She needs to: get a table for two, ask for the menu, order takoyaki and beer, ask for the bill. Guide her through step by step.",
  "taxi":       "\n\nSCENARIO: Taxi in Kumamoto. She needs to get from Kumamoto Station to Kumamoto Castle (熊本城). Practice hailing the taxi, telling the driver the destination, and paying.",
  "onsen":      "\n\nSCENARIO: Onsen at Kurokawa Onsen near Kumamoto. She wants to book a private bath (貸切風呂) and ask about the facilities. Also teach 2-3 onsen etiquette rules she should know.",
  "shopping":   "\n\nSCENARIO: Shopping in Osaka's Shinsaibashi. She wants to buy omiyage (souvenirs) for family. Practice: looking at items, asking for sizes, paying, asking about tax-free, requesting gift wrapping.",
  "shrine":     "\n\nSCENARIO: Visiting Fushimi Inari Shrine in Kyoto. Teach her the proper visiting sequence: temizu hand-washing, bowing, offerings, omikuji. Use the actual Japanese terms.",
  "emergency":  "\n\nSCENARIO: Emergency phrases. Go through the most critical situations: lost, feeling sick, need a doctor, lost passport, need police. One at a time, drill each phrase until she has it.",
  "shinkansen": "\n\nSCENARIO: Taking the Shinkansen. She needs to travel from Osaka to Tokyo. Practice: buying a ticket, finding the platform, asking which car, storing luggage, and asking a conductor a question.",
  "konbini":    "\n\nSCENARIO: At a 7-Eleven in Tokyo. She wants to buy onigiri, ask for it to be heated, and pay with cash. Also teach her the standard konbini phrases she'll hear from staff.",
  "kansai":     "\n\nSCENARIO: Kansai-ben (Osaka dialect) special lesson! Teach her 5 Osaka dialect phrases that will delight locals: おおきに, めっちゃ, なんでやねん, ほんま, でっせ. Give context for each one.",
  "honeymoon":  "\n\nSCENARIO: Honeymoon phrases. She just got married! Teach her how to say they're on their honeymoon (新婚旅行), introduce her husband, mention it's a special occasion, and how to ask for something romantic.",
}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    scenario: str = "general"

@router.post("/message")
async def chat(data: ChatRequest, user: User = Depends(get_current_user)):
    if not ANTHROPIC_API_KEY:
        return {"reply": "⚠️ ANTHROPIC_API_KEY not set. Add it to backend/.env to use AI Sensei."}
    scenario_ctx = SCENARIO_PROMPTS.get(data.scenario, "")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 400,
                "system": SYSTEM_PROMPT + scenario_ctx,
                "messages": [{"role": m.role, "content": m.content} for m in data.messages]
            }
        )
    result = resp.json()
    reply = result.get("content", [{}])[0].get("text", "Something went wrong.")
    return {"reply": reply}

@router.get("/scenarios")
async def list_scenarios(user: User = Depends(get_current_user)):
    return [
      {"id":"general",    "label":"💬 Free chat",            "desc":"Open conversation with Usui-sensei"},
      {"id":"business",   "label":"🤝 Business intro",        "desc":"3-level self-introduction practice"},
      {"id":"hotel",      "label":"🏨 Ryokan check-in",       "desc":"Kyoto traditional inn arrival"},
      {"id":"restaurant", "label":"🍣 Osaka izakaya",         "desc":"Order food, drinks, ask for bill"},
      {"id":"taxi",       "label":"🚕 Kumamoto taxi",         "desc":"Directions to the castle"},
      {"id":"onsen",      "label":"♨️ Onsen etiquette",       "desc":"Kurokawa Onsen booking + rules"},
      {"id":"shopping",   "label":"🛍️ Osaka shopping",        "desc":"Shinsaibashi omiyage shopping"},
      {"id":"shrine",     "label":"⛩️ Fushimi Inari",         "desc":"Shrine visit etiquette in Kyoto"},
      {"id":"emergency",  "label":"🆘 Emergency phrases",     "desc":"Lost, sick, need help"},
      {"id":"shinkansen", "label":"🚅 Shinkansen",            "desc":"Bullet train Osaka → Tokyo"},
      {"id":"konbini",    "label":"🏪 Konbini",               "desc":"7-Eleven in Tokyo"},
      {"id":"kansai",     "label":"😄 Kansai-ben",            "desc":"Osaka dialect phrases for locals"},
      {"id":"honeymoon",  "label":"💑 Honeymoon phrases",     "desc":"Announcing the big trip"},
    ]
