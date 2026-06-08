from datetime import datetime, timedelta
from models.flashcard import Flashcard

def sm2(card: Flashcard, rating: int) -> Flashcard:
    """
    SM-2 algorithm.
    rating: 0=complete blackout, 1=wrong, 2=hard, 3=ok, 4=good, 5=easy
    """
    if rating >= 3:
        if card.repetitions == 0:
            interval = 1
        elif card.repetitions == 1:
            interval = 6
        else:
            interval = round(card.interval * card.ease_factor)
        card.repetitions += 1
    else:
        card.repetitions = 0
        interval = 1

    ease_factor = card.ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
    card.ease_factor = max(1.3, ease_factor)
    card.interval = interval
    next_review_date = datetime.utcnow() + timedelta(days=interval)
    card.next_review = next_review_date.strftime("%Y-%m-%d")
    return card

def get_due_cards_query(user_id: str, today: str):
    """Return cards due today or overdue."""
    return Flashcard.find(
        Flashcard.user_id == user_id,
        Flashcard.next_review <= today
    )
