from fastapi import APIRouter, Depends
from models.user import User
from services.auth_service import get_current_user
from typing import Optional

router = APIRouter()

CURATED_CONTENT = [
  # ── ANIME ──────────────────────────────────────────────────────────────────
  {"title":"Chi's Sweet Home (チーズスイートホーム)","type":"anime",
   "url":"https://www.crunchyroll.com/chis-sweet-home",
   "description":"3-minute episodes about a lost kitten finding a home. Extremely clear, slow speech — perfect for total beginners. You'll learn household vocabulary and basic daily expressions.",
   "difficulty":"beginner","duration_minutes":3,"city_tag":"","tags":["beginner","short","household","cute"]},

  {"title":"Shirokuma Cafe (しろくまカフェ)","type":"anime",
   "url":"https://www.crunchyroll.com",
   "description":"A polar bear runs a cozy café. Slow, clear speech with lots of food and café vocabulary. Great for learning how Japanese people talk in casual settings.",
   "difficulty":"beginner","duration_minutes":22,"city_tag":"","tags":["cafe","food","beginner","vocabulary"]},

  {"title":"Yotsuba&! (よつばと！) anime clips","type":"anime",
   "url":"https://www.youtube.com/results?search_query=yotsuba+japanese",
   "description":"A curious 5-year-old explores the world. Native child-directed speech is ideal for comprehensible input — natural, warm, and packed with everyday vocabulary.",
   "difficulty":"beginner","duration_minutes":5,"city_tag":"","tags":["daily-life","children","CI","beginner"]},

  {"title":"My Neighbor Totoro (となりのトトロ) — clip practice","type":"anime",
   "url":"https://www.youtube.com/results?search_query=totoro+japanese+scene",
   "description":"Watch iconic Ghibli scenes in Japanese. Familiar visuals make comprehension easier — great CI with emotional engagement that helps memory.",
   "difficulty":"elementary","duration_minutes":5,"city_tag":"","tags":["ghibli","family","CI","emotional"]},

  {"title":"Spirited Away (千と千尋の神隠し) — scene practice","type":"anime",
   "url":"https://www.youtube.com/results?search_query=spirited+away+japanese+onsen+scene",
   "description":"The onsen/bathhouse scenes are perfect for learning service industry language and polite requests. Highly relevant to her ryokan and onsen experiences.",
   "difficulty":"elementary","duration_minutes":8,"city_tag":"kumamoto","tags":["onsen","ghibli","service","hotel"]},

  # ── DRAMA ──────────────────────────────────────────────────────────────────
  {"title":"Midnight Diner (深夜食堂)","type":"drama",
   "url":"https://www.netflix.com/title/80113037",
   "description":"A late-night Tokyo diner serves lonely regulars. Quiet, intimate, authentic everyday Japanese. Packed with food vocabulary and warm casual conversation. Perfect for learning restaurant and konbini culture.",
   "difficulty":"elementary","duration_minutes":25,"city_tag":"tokyo","tags":["food","tokyo","slice-of-life","restaurant","authentic"]},

  {"title":"Terrace House — Opening New Doors","type":"drama",
   "url":"https://www.netflix.com/title/80177667",
   "description":"Real people living together, having natural unscripted conversations. The best show for hearing authentic everyday Japanese speech patterns, not actor-polished dialogue.",
   "difficulty":"elementary","duration_minutes":45,"city_tag":"","tags":["conversation","authentic","daily-life","natural-speech"]},

  {"title":"Samurai Gourmet (サムライグルメ)","type":"drama",
   "url":"https://www.netflix.com/title/80113005",
   "description":"A retired salaryman rediscovers Japanese food culture. Beautiful food scenes, clear speech, warm story. Perfect for restaurant vocabulary and understanding food culture.",
   "difficulty":"elementary","duration_minutes":22,"city_tag":"","tags":["food","culture","retired","restaurant","drama"]},

  {"title":"Ainori Love Wagon: Asian Journey","type":"drama",
   "url":"https://www.netflix.com/title/81002595",
   "description":"Japanese dating reality show — natural conversation, romance vocabulary, and emotional expressions. Fun and relevant for a couple learning Japanese together.",
   "difficulty":"elementary","duration_minutes":45,"city_tag":"","tags":["romance","conversation","natural","couple"]},

  {"title":"Grand Maison Tokyo (グランメゾン東京)","type":"drama",
   "url":"https://www.netflix.com",
   "description":"Drama about elite chefs aiming for a Michelin star. Dense food vocabulary, kitchen language, and Tokyo restaurant culture. Great for dining scenario prep.",
   "difficulty":"intermediate","duration_minutes":60,"city_tag":"tokyo","tags":["food","restaurant","tokyo","advanced-vocab"]},

  # ── PODCAST ────────────────────────────────────────────────────────────────
  {"title":"Nihongo con Teppei for Beginners","type":"podcast",
   "url":"https://open.spotify.com/show/0cCFaKi0OXXlBNVqKKhTME",
   "description":"5–10 minute episodes in slow, clear Japanese specifically for beginners. Perfect for walks, commutes, or doing dishes. Teppei explains daily life topics naturally.",
   "difficulty":"beginner","duration_minutes":8,"city_tag":"","tags":["beginner","listening","commute","daily","free"]},

  {"title":"JapanesePod101 — Absolute Beginner","type":"podcast",
   "url":"https://www.japanesepod101.com/japanese-for-absolute-beginners/",
   "description":"Structured lessons with cultural insights. Good for filling gaps between Usui-sensei's classes. Has specific travel conversation series.",
   "difficulty":"beginner","duration_minutes":15,"city_tag":"","tags":["structured","beginner","cultural","travel"]},

  {"title":"Learn Japanese Pod","type":"podcast",
   "url":"https://learnjapanesepod.com",
   "description":"Conversational Japanese lessons with dialogue examples. Good intermediate listening bridge after completing the Showa Boston course.",
   "difficulty":"elementary","duration_minutes":20,"city_tag":"","tags":["dialogue","intermediate","conversational"]},

  {"title":"Erin's Challenge (エリンが挑戦！)","type":"podcast",
   "url":"https://www.erin.ne.jp/en/",
   "description":"Free Japan Foundation resource. Erin navigates real Japanese daily life situations — school, shopping, transport. With video and transcript. Highly practical.",
   "difficulty":"elementary","duration_minutes":15,"city_tag":"","tags":["practical","japan-foundation","free","daily-life","structured"]},

  {"title":"NHK World Easy Japanese — audio","type":"podcast",
   "url":"https://www3.nhk.or.jp/nhkworld/en/learnjapanese/",
   "description":"NHK's structured beginner course. 48 episodes covering travel, daily life, and culture. Free. Comes with scripts. Built exactly for travelers visiting Japan.",
   "difficulty":"beginner","duration_minutes":10,"city_tag":"","tags":["nhk","travel","structured","free","48-episodes"]},

  # ── COOKING SHOWS ──────────────────────────────────────────────────────────
  {"title":"Cooking with Dog","type":"cooking",
   "url":"https://www.youtube.com/@cookingwithdog",
   "description":"Classic Japanese home cooking YouTube channel narrated by a poodle. Slow, clear Japanese with food vocabulary. Learn ingredients, verbs, and kitchen culture at once.",
   "difficulty":"beginner","duration_minutes":12,"city_tag":"","tags":["food","cooking","vocabulary","youtube","home-cooking"]},

  {"title":"NHK World — Dining with the Chef","type":"cooking",
   "url":"https://www3.nhk.or.jp/nhkworld/en/tv/dining/",
   "description":"Professional NHK cooking show, free online. Switch audio to Japanese and toggle English subtitles. Covers regional Japanese cuisines including Kyushu dishes.",
   "difficulty":"elementary","duration_minutes":28,"city_tag":"","tags":["cooking","nhk","free","regional","kyushu"]},

  {"title":"Osaka Street Food Tour — Japanese narration","type":"cooking",
   "url":"https://www.youtube.com/results?search_query=osaka+street+food+japanese+narration",
   "description":"YouTube food tours of Dotonbori narrated in Japanese. Hear real Osaka food vocabulary and casual speech in context. Also great motivation for the trip.",
   "difficulty":"elementary","duration_minutes":15,"city_tag":"osaka","tags":["osaka","street-food","dotonbori","vocabulary","motivation"]},

  {"title":"Kyoto Kaiseki Cooking — Japanese","type":"cooking",
   "url":"https://www.youtube.com/results?search_query=kyoto+kaiseki+japanese",
   "description":"Kaiseki is Kyoto's multi-course haute cuisine — vocabulary you'll actually encounter at a ryokan dinner. Watch in Japanese to hear formal dining language.",
   "difficulty":"intermediate","duration_minutes":20,"city_tag":"kyoto","tags":["kyoto","ryokan","kaiseki","formal-dining","vocabulary"]},

  # ── YOUTUBE ────────────────────────────────────────────────────────────────
  {"title":"Paolo fromTOKYO — Tokyo walking tours","type":"youtube",
   "url":"https://www.youtube.com/@PaolofromTOKYO",
   "description":"High-quality Tokyo daily life and food vlogs. Great for hearing natural speech and seeing exactly where she'll visit. Switch to JP audio + JP subtitles for CI practice.",
   "difficulty":"elementary","duration_minutes":15,"city_tag":"tokyo","tags":["tokyo","walking-tour","daily-life","food","motivation"]},

  {"title":"Abroad in Japan — Kyoto episode","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=abroad+in+japan+kyoto",
   "description":"Chris Broad's documentary-style Japan videos. Watch in English first for content, then again in Japanese audio. His Kyoto temple content is stunning.",
   "difficulty":"elementary","duration_minutes":20,"city_tag":"kyoto","tags":["kyoto","temples","english-friendly","documentary"]},

  {"title":"Kumamoto Travel Vlog — Japanese narration","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=熊本+観光+vlog",
   "description":"Search 熊本 観光 vlog on YouTube. Hear local Kumamoto speech, see the castle, and pick up region-specific vocabulary. Bonus: Kumamon sightings guaranteed.",
   "difficulty":"elementary","duration_minutes":15,"city_tag":"kumamoto","tags":["kumamoto","castle","kumamon","local-speech","motivation"]},

  {"title":"Osaka Dotonbori night walk — Japanese","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=大阪+道頓堀+夜+vlog",
   "description":"Search 大阪 道頓堀 夜 vlog. Evening walks through Osaka's entertainment district — hear Kansai dialect in the wild, see takoyaki stalls, neon signs.",
   "difficulty":"elementary","duration_minutes":12,"city_tag":"osaka","tags":["osaka","dotonbori","night","kansai-ben","street-food"]},

  {"title":"Kyoto Ryokan Experience — full tour","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=kyoto+ryokan+japanese+experience",
   "description":"Full ryokan experience videos in Japanese. Watch before her Kyoto stay — learn check-in etiquette, yukata, kaiseki dinner, and onsen vocabulary.",
   "difficulty":"elementary","duration_minutes":20,"city_tag":"kyoto","tags":["ryokan","kyoto","check-in","onsen","etiquette"]},

  {"title":"Tokyo Train System Explained — Japanese","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=tokyo+train+system+japanese+tutorial",
   "description":"Tokyo's train network is overwhelming — watching a guide in Japanese before the trip builds vocabulary and reduces travel anxiety. Suica, JR Pass, transfers.",
   "difficulty":"elementary","duration_minutes":12,"city_tag":"tokyo","tags":["tokyo","train","suica","navigation","anxiety-reducing"]},

  {"title":"Onsen Etiquette Guide — Japanese","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=温泉+マナー+入り方+日本語",
   "description":"Search 温泉 マナー 入り方 日本語. Learn proper onsen etiquette in Japanese — vocabulary you'll hear at Kurokawa Onsen and the ryokan. Critical for a comfortable stay.",
   "difficulty":"beginner","duration_minutes":8,"city_tag":"kumamoto","tags":["onsen","etiquette","kurokawa","kumamoto","manners"]},

  {"title":"Japanese Temple Etiquette (お参りの作法)","type":"youtube",
   "url":"https://www.youtube.com/results?search_query=神社+参拝+作法+日本語",
   "description":"How to properly visit a Shinto shrine — washing hands, bowing, clapping, omikuji. In Japanese with clear demonstrations. Essential for Fushimi Inari visits.",
   "difficulty":"beginner","duration_minutes":7,"city_tag":"kyoto","tags":["shrine","temple","etiquette","kyoto","fushimi-inari"]},

  # ── SHORT STORIES / READING ─────────────────────────────────────────────
  {"title":"Tadoku Free Graded Readers — Level 0","type":"shortStory",
   "url":"https://tadoku.org/japanese/en/free-books-en/",
   "description":"Completely free graded readers from the Tadoku project. Level 0 has ~50 words per story with furigana. Perfect for early reading practice. Download PDFs.",
   "difficulty":"beginner","duration_minutes":10,"city_tag":"","tags":["reading","free","graded-reader","furigana","pdf"]},

  {"title":"Tadoku Graded Readers — Level 1","type":"shortStory",
   "url":"https://tadoku.org/japanese/en/free-books-en/",
   "description":"Short stories at slightly higher difficulty. Covers daily life scenarios including eating out, shopping, and travel — directly relevant to the honeymoon trip.",
   "difficulty":"elementary","duration_minutes":15,"city_tag":"","tags":["reading","free","graded-reader","travel","shopping"]},

  {"title":"NHK Web Easy News (やさしい日本語)","type":"shortStory",
   "url":"https://www3.nhk.or.jp/news/easy/",
   "description":"NHK News written in simple Japanese for learners and children. Free, updated daily. Start just reading headlines — they are 5–10 words each and very achievable.",
   "difficulty":"elementary","duration_minutes":10,"city_tag":"","tags":["news","current-events","nhk","free","daily","hiragana"]},

  {"title":"Kyoto Travel Story — Watanabe Misa Graded Reader","type":"shortStory",
   "url":"https://www.amazon.com/s?k=japanese+graded+reader+kyoto",
   "description":"Short travel stories set in Kyoto written for learners at beginner-intermediate level. Reading a story set in her actual destination boosts motivation and memory.",
   "difficulty":"elementary","duration_minutes":20,"city_tag":"kyoto","tags":["kyoto","reading","travel","graded-reader","motivation"]},
]

@router.get("/")
async def get_content(
    type: Optional[str] = None,
    city: Optional[str] = None,
    difficulty: Optional[str] = None,
    user: User = Depends(get_current_user)
):
    items = CURATED_CONTENT
    if type:       items = [i for i in items if i["type"] == type]
    if city:       items = [i for i in items if i.get("city_tag") == city or city in i.get("tags", [])]
    if difficulty: items = [i for i in items if i["difficulty"] == difficulty]
    return items

@router.get("/types")
async def content_types(user: User = Depends(get_current_user)):
    return sorted(set(i["type"] for i in CURATED_CONTENT))

@router.get("/stats")
async def content_stats(user: User = Depends(get_current_user)):
    by_type = {}
    by_city = {}
    for i in CURATED_CONTENT:
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1
        if i.get("city_tag"):
            by_city[i["city_tag"]] = by_city.get(i["city_tag"], 0) + 1
    return {"total": len(CURATED_CONTENT), "by_type": by_type, "by_city": by_city}
