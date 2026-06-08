from fastapi import APIRouter, Depends, HTTPException
from models.flashcard import Flashcard, FlashcardCreate, FlashcardReview, ReviewSubmit
from models.user import User
from models.progress import ProgressEntry
from services.auth_service import get_current_user
from services.srs_service import sm2
from datetime import datetime
from typing import List

router = APIRouter()

# ─── 150+ seed cards covering full honeymoon trip ───────────────────────────

SEED_CARDS = [
  # ── WEEK 1: Business Introductions (Usui-sensei) ──────────────────────────
  {"front":"はじめまして","front_reading":"hajimemashite","back":"Nice to meet you","example":"はじめまして、スミスです。","category":"business","city":""},
  {"front":"よろしくお願いします","front_reading":"yoroshiku onegaishimasu","back":"I look forward to working with you","example":"どうぞよろしくお願いします。","category":"business","city":""},
  {"front":"申します","front_reading":"moushimasu","back":"My name is... (humble/formal)","example":"スミスと申します。","category":"business","city":""},
  {"front":"名刺","front_reading":"meishi","back":"Business card","example":"名刺をどうぞ。","category":"business","city":""},
  {"front":"よろしくお願いいたします","front_reading":"yoroshiku onegai itashimasu","back":"I humbly look forward to your favor (very formal)","example":"どうぞよろしくお願いいたします。","category":"business","city":""},
  {"front":"所属しております","front_reading":"shozoku shite orimasu","back":"I belong to / I am affiliated with","example":"ソフトウェア開発部に所属しております。","category":"business","city":""},
  {"front":"お辞儀","front_reading":"ojigi","back":"Bowing","example":"お辞儀をしてください。","category":"business","city":""},

  # ── WEEK 2: Office visit / meeting people ─────────────────────────────────
  {"front":"いらっしゃいませ","front_reading":"irasshaimase","back":"Welcome! (formal greeting to customers)","example":"いらっしゃいませ！","category":"business","city":""},
  {"front":"お待ちしております","front_reading":"omachi shite orimasu","back":"We are waiting for you (formal)","example":"三時にお待ちしております。","category":"business","city":""},
  {"front":"ご予約はございますか","front_reading":"goyoyaku wa gozaimasu ka","back":"Do you have a reservation?","example":"ご予約はございますか？","category":"business","city":""},
  {"front":"少々お待ちください","front_reading":"shoushou omachi kudasai","back":"Please wait a moment","example":"少々お待ちください。","category":"business","city":""},
  {"front":"ただいま参ります","front_reading":"tadaima mairimasu","back":"I will come right away","example":"ただいま参ります。","category":"business","city":""},

  # ── WEEK 3: Hotel / Ryokan ────────────────────────────────────────────────
  {"front":"チェックイン","front_reading":"chekku in","back":"Check-in","example":"チェックインをお願いします。","category":"hotel","city":""},
  {"front":"チェックアウト","front_reading":"chekku auto","back":"Check-out","example":"チェックアウトは何時ですか？","category":"hotel","city":""},
  {"front":"予約","front_reading":"yoyaku","back":"Reservation","example":"スミスの名前で予約しています。","category":"hotel","city":""},
  {"front":"部屋","front_reading":"heya","back":"Room","example":"部屋はどこですか？","category":"hotel","city":""},
  {"front":"旅館","front_reading":"ryokan","back":"Traditional Japanese inn","example":"京都の旅館に泊まりたいです。","category":"hotel","city":"kyoto"},
  {"front":"浴衣","front_reading":"yukata","back":"Light summer kimono (worn at ryokan)","example":"浴衣を着てもいいですか？","category":"hotel","city":"kyoto"},
  {"front":"布団","front_reading":"futon","back":"Traditional Japanese bedding on the floor","example":"布団を敷いてください。","category":"hotel","city":""},
  {"front":"鍵","front_reading":"kagi","back":"Key","example":"鍵をなくしました。","category":"hotel","city":""},
  {"front":"フロント","front_reading":"furonto","back":"Front desk / reception","example":"フロントに電話してください。","category":"hotel","city":""},
  {"front":"Wi-Fiのパスワード","front_reading":"waifai no pasuwado","back":"Wi-Fi password","example":"Wi-Fiのパスワードを教えてください。","category":"hotel","city":""},
  {"front":"荷物","front_reading":"nimotsu","back":"Luggage / baggage","example":"荷物を預かってもらえますか？","category":"hotel","city":""},
  {"front":"ルームサービス","front_reading":"ruumu saabiisu","back":"Room service","example":"ルームサービスをお願いします。","category":"hotel","city":""},

  # ── WEEK 4: Dining / Restaurants ─────────────────────────────────────────
  {"front":"いただきます","front_reading":"itadakimasu","back":"Let's eat (said before meals)","example":"いただきます！","category":"food","city":""},
  {"front":"ごちそうさまでした","front_reading":"gochisousama deshita","back":"Thank you for the meal (said after eating)","example":"ごちそうさまでした！","category":"food","city":""},
  {"front":"メニュー","front_reading":"menyuu","back":"Menu","example":"メニューをください。","category":"food","city":""},
  {"front":"おすすめ","front_reading":"osusume","back":"Recommendation","example":"おすすめは何ですか？","category":"food","city":""},
  {"front":"お会計","front_reading":"okaikei","back":"The bill / check","example":"お会計をお願いします。","category":"food","city":""},
  {"front":"一つください","front_reading":"hitotsu kudasai","back":"One please","example":"たこ焼きを一つください。","category":"food","city":""},
  {"front":"おいしい","front_reading":"oishii","back":"Delicious","example":"これはおいしいです！","category":"food","city":""},
  {"front":"辛い","front_reading":"karai","back":"Spicy","example":"辛いものが苦手です。","category":"food","city":""},
  {"front":"アレルギー","front_reading":"arerugii","back":"Allergy","example":"えびアレルギーがあります。","category":"food","city":""},
  {"front":"ベジタリアン","front_reading":"bejitarian","back":"Vegetarian","example":"ベジタリアンです。","category":"food","city":""},
  {"front":"禁煙席","front_reading":"kinen seki","back":"Non-smoking seat","example":"禁煙席をお願いします。","category":"food","city":""},
  {"front":"二人です","front_reading":"futari desu","back":"Two people / a table for two","example":"二人ですが、席はありますか？","category":"food","city":""},
  {"front":"お箸","front_reading":"ohashi","back":"Chopsticks","example":"お箸をください。","category":"food","city":""},
  {"front":"水","front_reading":"mizu","back":"Water","example":"お水をください。","category":"food","city":""},
  {"front":"ビール","front_reading":"biiru","back":"Beer","example":"ビールを二つください。","category":"food","city":""},
  {"front":"乾杯","front_reading":"kanpai","back":"Cheers!","example":"乾杯！","category":"food","city":""},

  # ── WEEK 5: Getting around / transport ───────────────────────────────────
  {"front":"タクシー","front_reading":"takushii","back":"Taxi","example":"タクシーをお願いします。","category":"transport","city":""},
  {"front":"電車","front_reading":"densha","back":"Train","example":"電車はどこですか？","category":"transport","city":""},
  {"front":"新幹線","front_reading":"shinkansen","back":"Bullet train","example":"新幹線に乗りたいです。","category":"transport","city":""},
  {"front":"バス","front_reading":"basu","back":"Bus","example":"バスで行けますか？","category":"transport","city":""},
  {"front":"駅","front_reading":"eki","back":"Station","example":"駅はどこですか？","category":"transport","city":""},
  {"front":"切符","front_reading":"kippu","back":"Ticket","example":"切符をください。","category":"transport","city":""},
  {"front":"〜まで","front_reading":"〜made","back":"To / until (destination)","example":"京都までいくらですか？","category":"transport","city":""},
  {"front":"右","front_reading":"migi","back":"Right","example":"右に曲がってください。","category":"transport","city":""},
  {"front":"左","front_reading":"hidari","back":"Left","example":"左に曲がってください。","category":"transport","city":""},
  {"front":"まっすぐ","front_reading":"massugu","back":"Straight ahead","example":"まっすぐ行ってください。","category":"transport","city":""},
  {"front":"近い","front_reading":"chikai","back":"Near / close","example":"駅は近いですか？","category":"transport","city":""},
  {"front":"遠い","front_reading":"tooi","back":"Far","example":"ホテルは遠いですか？","category":"transport","city":""},
  {"front":"地図","front_reading":"chizu","back":"Map","example":"地図を見せてください。","category":"transport","city":""},
  {"front":"迷いました","front_reading":"mayoimashita","back":"I got lost","example":"すみません、迷いました。","category":"transport","city":""},
  {"front":"乗り換え","front_reading":"noriakae","back":"Transfer (train)","example":"乗り換えはどこですか？","category":"transport","city":""},
  {"front":"ICカード","front_reading":"IC kaado","back":"IC card (Suica/ICOCA transit card)","example":"ICカードで払えますか？","category":"transport","city":""},

  # ── GENERAL / ESSENTIAL ───────────────────────────────────────────────────
  {"front":"ありがとうございます","front_reading":"arigatou gozaimasu","back":"Thank you (formal)","example":"どうもありがとうございます。","category":"general","city":""},
  {"front":"すみません","front_reading":"sumimasen","back":"Excuse me / I'm sorry","example":"すみません、駅はどこですか？","category":"general","city":""},
  {"front":"わかりません","front_reading":"wakarimasen","back":"I don't understand","example":"すみません、わかりません。","category":"general","city":""},
  {"front":"もう一度お願いします","front_reading":"mou ichido onegaishimasu","back":"Please say that again","example":"すみません、もう一度お願いします。","category":"general","city":""},
  {"front":"ゆっくり話してください","front_reading":"yukkuri hanashite kudasai","back":"Please speak slowly","example":"ゆっくり話してください。","category":"general","city":""},
  {"front":"日本語が少しわかります","front_reading":"nihongo ga sukoshi wakarimasu","back":"I understand a little Japanese","example":"日本語が少しわかります。","category":"general","city":""},
  {"front":"英語を話せますか","front_reading":"eigo wo hanasemasu ka","back":"Can you speak English?","example":"すみません、英語を話せますか？","category":"general","city":""},
  {"front":"はい","front_reading":"hai","back":"Yes / I understand","example":"はい、わかりました。","category":"general","city":""},
  {"front":"いいえ","front_reading":"iie","back":"No","example":"いいえ、結構です。","category":"general","city":""},
  {"front":"いくらですか","front_reading":"ikura desu ka","back":"How much is it?","example":"これはいくらですか？","category":"general","city":""},
  {"front":"どこですか","front_reading":"doko desu ka","back":"Where is...?","example":"トイレはどこですか？","category":"general","city":""},
  {"front":"〜に行きたいです","front_reading":"〜ni ikitai desu","back":"I want to go to...","example":"熊本城に行きたいです。","category":"general","city":""},
  {"front":"写真を撮ってもいいですか","front_reading":"shashin wo totte mo ii desu ka","back":"May I take a photo?","example":"ここで写真を撮ってもいいですか？","category":"general","city":""},
  {"front":"助けてください","front_reading":"tasukete kudasai","back":"Please help me","example":"すみません、助けてください！","category":"emergency","city":""},
  {"front":"救急車","front_reading":"kyuukyuusha","back":"Ambulance","example":"救急車を呼んでください！","category":"emergency","city":""},
  {"front":"病院","front_reading":"byouin","back":"Hospital","example":"病院に行きたいです。","category":"emergency","city":""},
  {"front":"薬","front_reading":"kusuri","back":"Medicine","example":"薬はどこで買えますか？","category":"emergency","city":""},
  {"front":"パスポート","front_reading":"pasupooto","back":"Passport","example":"パスポートをなくしました。","category":"emergency","city":""},

  # ── OSAKA SPECIFIC ────────────────────────────────────────────────────────
  {"front":"たこ焼き","front_reading":"takoyaki","back":"Takoyaki (Osaka octopus balls)","example":"たこ焼きを二つください。","category":"food","city":"osaka"},
  {"front":"お好み焼き","front_reading":"okonomiyaki","back":"Savory pancake (Osaka specialty)","example":"お好み焼きを食べたいです。","category":"food","city":"osaka"},
  {"front":"道頓堀","front_reading":"dotonbori","back":"Dotonbori (Osaka entertainment district)","example":"道頓堀に行きたいです。","category":"travel","city":"osaka"},
  {"front":"大阪城","front_reading":"osakajou","back":"Osaka Castle","example":"大阪城はどこですか？","category":"travel","city":"osaka"},
  {"front":"おおきに","front_reading":"ookini","back":"Thank you (Kansai dialect)","example":"おおきに！(Osaka way to say ありがとう)","category":"kansai-ben","city":"osaka"},
  {"front":"めっちゃ","front_reading":"meccha","back":"Very / extremely (Kansai dialect)","example":"めっちゃおいしい！","category":"kansai-ben","city":"osaka"},
  {"front":"なんでやねん","front_reading":"nande yanen","back":"Why! / No way! (Kansai comedic expression)","example":"なんでやねん！(classic Osaka retort)","category":"kansai-ben","city":"osaka"},
  {"front":"でっせ","front_reading":"desse","back":"It is (Kansai dialect for です)","example":"ほんまでっせ。","category":"kansai-ben","city":"osaka"},
  {"front":"心斎橋","front_reading":"shinsaibashi","back":"Shinsaibashi (Osaka shopping street)","example":"心斎橋でショッピングしましょう。","category":"travel","city":"osaka"},

  # ── KYOTO SPECIFIC ────────────────────────────────────────────────────────
  {"front":"伏見稲荷","front_reading":"fushimi inari","back":"Fushimi Inari Shrine (famous torii gates)","example":"伏見稲荷大社に行きたいです。","category":"travel","city":"kyoto"},
  {"front":"嵐山","front_reading":"arashiyama","back":"Arashiyama (Kyoto bamboo grove district)","example":"嵐山はどこですか？","category":"travel","city":"kyoto"},
  {"front":"金閣寺","front_reading":"kinkakuji","back":"Kinkakuji (Golden Pavilion)","example":"金閣寺を見たいです。","category":"travel","city":"kyoto"},
  {"front":"抹茶","front_reading":"matcha","back":"Matcha (powdered green tea)","example":"抹茶のアイスをください。","category":"food","city":"kyoto"},
  {"front":"お寺","front_reading":"otera","back":"Buddhist temple","example":"このお寺は有名ですか？","category":"travel","city":"kyoto"},
  {"front":"神社","front_reading":"jinja","back":"Shinto shrine","example":"神社でお参りしたいです。","category":"travel","city":"kyoto"},
  {"front":"着物","front_reading":"kimono","back":"Kimono","example":"着物を着てみたいです。","category":"travel","city":"kyoto"},
  {"front":"祇園","front_reading":"gion","back":"Gion (Kyoto's geisha district)","example":"祇園を散歩したいです。","category":"travel","city":"kyoto"},
  {"front":"おみくじ","front_reading":"omikuji","back":"Fortune slip (drawn at shrines/temples)","example":"おみくじを引きたいです。","category":"travel","city":"kyoto"},
  {"front":"お守り","front_reading":"omamori","back":"Lucky charm / amulet","example":"お守りを買いたいです。","category":"travel","city":"kyoto"},
  {"front":"拝観料","front_reading":"haikanryou","back":"Admission / entrance fee (temples)","example":"拝観料はいくらですか？","category":"travel","city":"kyoto"},

  # ── TOKYO SPECIFIC ────────────────────────────────────────────────────────
  {"front":"渋谷","front_reading":"shibuya","back":"Shibuya (Tokyo shopping/crossing district)","example":"渋谷スクランブル交差点は有名です。","category":"travel","city":"tokyo"},
  {"front":"浅草","front_reading":"asakusa","back":"Asakusa (Tokyo's historic temple area)","example":"浅草に行きたいです。","category":"travel","city":"tokyo"},
  {"front":"東京タワー","front_reading":"toukyou tawaa","back":"Tokyo Tower","example":"東京タワーが見たいです。","category":"travel","city":"tokyo"},
  {"front":"山手線","front_reading":"yamanote sen","back":"Yamanote Line (Tokyo's main loop train)","example":"山手線に乗ってください。","category":"transport","city":"tokyo"},
  {"front":"コンビニ","front_reading":"konbini","back":"Convenience store (7-11, FamilyMart, Lawson)","example":"コンビニはどこですか？","category":"general","city":"tokyo"},
  {"front":"温めてください","front_reading":"atatamete kudasai","back":"Please heat this up (at konbini)","example":"これを温めてください。","category":"food","city":"tokyo"},
  {"front":"袋は要りません","front_reading":"fukuro wa irimasen","back":"I don't need a bag","example":"袋は要りません、ありがとうございます。","category":"general","city":"tokyo"},
  {"front":"スイカ","front_reading":"suika","back":"Suica (Tokyo IC transit card)","example":"スイカで払います。","category":"transport","city":"tokyo"},
  {"front":"秋葉原","front_reading":"akihabara","back":"Akihabara (Tokyo electronics/anime district)","example":"秋葉原に行ったことがありますか？","category":"travel","city":"tokyo"},
  {"front":"新宿","front_reading":"shinjuku","back":"Shinjuku (Tokyo major hub)","example":"新宿駅はどこですか？","category":"transport","city":"tokyo"},

  # ── KUMAMOTO SPECIFIC ────────────────────────────────────────────────────
  {"front":"熊本城","front_reading":"kumamotojou","back":"Kumamoto Castle","example":"熊本城はどこですか？","category":"travel","city":"kumamoto"},
  {"front":"くまモン","front_reading":"kumamon","back":"Kumamon (Kumamoto's bear mascot)","example":"くまモンのグッズを買いたいです。","category":"travel","city":"kumamoto"},
  {"front":"馬刺し","front_reading":"basashi","back":"Raw horse meat (Kumamoto specialty)","example":"馬刺しを試してみたいです。","category":"food","city":"kumamoto"},
  {"front":"熊本ラーメン","front_reading":"kumamoto raamen","back":"Kumamoto ramen (garlic tonkotsu)","example":"熊本ラーメンを食べたいです。","category":"food","city":"kumamoto"},
  {"front":"阿蘇山","front_reading":"aso san","back":"Mount Aso (active volcano near Kumamoto)","example":"阿蘇山に行きたいです。","category":"travel","city":"kumamoto"},
  {"front":"水前寺公園","front_reading":"suizenji kouen","back":"Suizenji Garden (Kumamoto)","example":"水前寺公園はきれいですね。","category":"travel","city":"kumamoto"},
  {"front":"黒川温泉","front_reading":"kurokawa onsen","back":"Kurokawa Onsen (hot spring town near Kumamoto)","example":"黒川温泉に行きたいです。","category":"onsen","city":"kumamoto"},

  # ── ONSEN / HOT SPRINGS ──────────────────────────────────────────────────
  {"front":"温泉","front_reading":"onsen","back":"Hot spring / onsen","example":"温泉に入りたいです。","category":"onsen","city":""},
  {"front":"露天風呂","front_reading":"rotenburo","back":"Outdoor hot spring bath","example":"露天風呂に入りましょう。","category":"onsen","city":""},
  {"front":"入浴料","front_reading":"nyuuyokuryou","back":"Bathing fee","example":"入浴料はいくらですか？","category":"onsen","city":""},
  {"front":"タオル","front_reading":"taoru","back":"Towel","example":"タオルを貸してもらえますか？","category":"onsen","city":""},
  {"front":"混浴","front_reading":"kon'yoku","back":"Mixed gender bathing","example":"混浴の温泉はありますか？","category":"onsen","city":""},
  {"front":"貸切風呂","front_reading":"kashikiri buro","back":"Private bath (reserved just for you)","example":"貸切風呂を予約したいです。","category":"onsen","city":""},

  # ── SHOPPING ──────────────────────────────────────────────────────────────
  {"front":"見てもいいですか","front_reading":"mite mo ii desu ka","back":"May I look at this?","example":"見てもいいですか？","category":"shopping","city":""},
  {"front":"試着してもいいですか","front_reading":"shichaku shite mo ii desu ka","back":"May I try this on?","example":"これを試着してもいいですか？","category":"shopping","city":""},
  {"front":"大きいサイズ","front_reading":"ookii saizu","back":"Larger size","example":"大きいサイズはありますか？","category":"shopping","city":""},
  {"front":"クレジットカード","front_reading":"kurejitto kaado","back":"Credit card","example":"クレジットカードで払えますか？","category":"shopping","city":""},
  {"front":"現金","front_reading":"genkin","back":"Cash","example":"現金しか使えませんか？","category":"shopping","city":""},
  {"front":"免税","front_reading":"menzei","back":"Tax-free / duty-free","example":"免税できますか？","category":"shopping","city":""},
  {"front":"お土産","front_reading":"omiyage","back":"Souvenir","example":"お土産を探しています。","category":"shopping","city":""},
  {"front":"ラッピング","front_reading":"rappingu","back":"Gift wrapping","example":"ラッピングをお願いします。","category":"shopping","city":""},

  # ── HONEYMOON / ROMANTIC ─────────────────────────────────────────────────
  {"front":"新婚旅行","front_reading":"shinkon ryokou","back":"Honeymoon trip","example":"新婚旅行で日本に来ました。","category":"honeymoon","city":""},
  {"front":"結婚しました","front_reading":"kekkon shimashita","back":"We got married","example":"先月結婚しました。","category":"honeymoon","city":""},
  {"front":"夫","front_reading":"otto","back":"Husband (my husband)","example":"夫と一緒に来ました。","category":"honeymoon","city":""},
  {"front":"妻","front_reading":"tsuma","back":"Wife (my wife)","example":"妻のために買いたいです。","category":"honeymoon","city":""},
  {"front":"記念日","front_reading":"kinenbi","back":"Anniversary / special occasion","example":"今日は記念日です。","category":"honeymoon","city":""},
  {"front":"ロマンチック","front_reading":"romanchikku","back":"Romantic","example":"ロマンチックな場所はどこですか？","category":"honeymoon","city":""},
  {"front":"二人で","front_reading":"futari de","back":"Just the two of us","example":"二人でゆっくりしたいです。","category":"honeymoon","city":""},

  # ── NUMBERS / TIME ────────────────────────────────────────────────────────
  {"front":"何時ですか","front_reading":"nanji desu ka","back":"What time is it?","example":"すみません、何時ですか？","category":"general","city":""},
  {"front":"〜時に","front_reading":"〜ji ni","back":"At [time] o'clock","example":"三時にチェックインします。","category":"general","city":""},
  {"front":"今日","front_reading":"kyou","back":"Today","example":"今日はどこに行きますか？","category":"general","city":""},
  {"front":"明日","front_reading":"ashita","back":"Tomorrow","example":"明日チェックアウトします。","category":"general","city":""},
  {"front":"一","front_reading":"ichi","back":"One","example":"一つください。","category":"numbers","city":""},
  {"front":"二","front_reading":"ni","back":"Two","example":"二人です。","category":"numbers","city":""},
  {"front":"三","front_reading":"san","back":"Three","example":"三つください。","category":"numbers","city":""},
  {"front":"円","front_reading":"en","back":"Yen (Japanese currency)","example":"千円でお願いします。","category":"numbers","city":""},

  # ── TEMPLE / SHRINE ETIQUETTE ────────────────────────────────────────────
  {"front":"お参り","front_reading":"omairi","back":"Visiting / praying at a shrine or temple","example":"神社でお参りしましょう。","category":"culture","city":"kyoto"},
  {"front":"手水","front_reading":"temizu","back":"Purification water (wash hands at shrine)","example":"手水で手を清めましょう。","category":"culture","city":"kyoto"},
  {"front":"鳥居","front_reading":"torii","back":"Torii gate","example":"鳥居をくぐりましょう。","category":"culture","city":"kyoto"},
  {"front":"静かにしてください","front_reading":"shizuka ni shite kudasai","back":"Please be quiet","example":"ここでは静かにしてください。","category":"culture","city":""},
  {"front":"撮影禁止","front_reading":"satsuei kinshi","back":"No photography","example":"撮影禁止のサインがあります。","category":"culture","city":""},
]

router = APIRouter()

XP_PER_REVIEW = 5

@router.post("/seed")
async def seed_cards(user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    existing = await Flashcard.find(Flashcard.user_id == str(user.id)).count()
    if existing > 0:
        return {"message": "Cards already seeded", "count": existing}
    cards = [Flashcard(user_id=str(user.id), next_review=today,
                       front=c["front"], front_reading=c["front_reading"],
                       back=c["back"], example=c.get("example",""),
                       category=c.get("category","general"), city=c.get("city",""))
             for c in SEED_CARDS]
    await Flashcard.insert_many(cards)
    return {"message": f"Seeded {len(cards)} cards", "count": len(cards)}

@router.get("/due")
async def due_cards(user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    cards = await Flashcard.find(
        Flashcard.user_id == str(user.id),
        Flashcard.next_review <= today
    ).to_list()
    return [{"id": str(c.id), "front": c.front, "front_reading": c.front_reading,
             "back": c.back, "example": c.example, "category": c.category,
             "city": c.city, "interval": c.interval, "repetitions": c.repetitions} for c in cards]

@router.get("/all")
async def all_cards(user: User = Depends(get_current_user)):
    cards = await Flashcard.find(Flashcard.user_id == str(user.id)).to_list()
    return [{"id": str(c.id), "front": c.front, "front_reading": c.front_reading,
             "back": c.back, "category": c.category, "city": c.city,
             "next_review": c.next_review, "interval": c.interval} for c in cards]

@router.get("/stats")
async def card_stats(user: User = Depends(get_current_user)):
    cards = await Flashcard.find(Flashcard.user_id == str(user.id)).to_list()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    by_category = {}
    for c in cards:
        by_category[c.category] = by_category.get(c.category, 0) + 1
    by_city = {}
    for c in cards:
        if c.city:
            by_city[c.city] = by_city.get(c.city, 0) + 1
    return {
        "total": len(cards),
        "due_today": sum(1 for c in cards if c.next_review <= today),
        "mature": sum(1 for c in cards if c.interval >= 21),
        "learning": sum(1 for c in cards if c.interval < 21),
        "by_category": by_category,
        "by_city": by_city,
    }

@router.post("/review")
async def review_card(data: ReviewSubmit, user: User = Depends(get_current_user)):
    card = await Flashcard.get(data.card_id)
    if not card or card.user_id != str(user.id):
        raise HTTPException(404, "Card not found")
    card = sm2(card, data.rating)
    await card.save()
    await FlashcardReview(user_id=str(user.id), card_id=data.card_id, rating=data.rating).insert()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    entry = await ProgressEntry.find_one(
        ProgressEntry.user_id == str(user.id), ProgressEntry.date == today)
    if entry:
        entry.cards_reviewed += 1
        entry.xp_earned += XP_PER_REVIEW
        await entry.save()
    user_obj = await user.__class__.get(user.id)
    user_obj.xp = (user_obj.xp or 0) + XP_PER_REVIEW
    await user_obj.save()
    return {"next_review": card.next_review, "interval": card.interval, "ease": round(card.ease_factor, 2)}

@router.post("/add")
async def add_card(data: FlashcardCreate, user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    card = Flashcard(user_id=str(user.id), next_review=today, **data.dict())
    await card.insert()
    return {"id": str(card.id), "message": "Card added"}
