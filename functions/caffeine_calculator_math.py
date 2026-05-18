import re
import unicodedata
from difflib import SequenceMatcher


PEAK_MINUTES = 45
CRASH_HOURS = 4
RECOVERY_HOURS = 8
BASE_EFFECT_HOURS = 3.0
REFERENCE_CAFFEINE_MG = 80
MAX_EFFECT_HOURS = 6.0


def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]", "", text)
    return text


def search_matches(search_text, drink_name):
    if search_text.strip() == "":
        return True

    search_clean = normalize_text(search_text)
    drink_clean = normalize_text(drink_name)

    if search_clean in drink_clean:
        return True

    similarity = SequenceMatcher(None, search_clean, drink_clean).ratio()
    return similarity >= 0.45


def caffeine_effect_duration_hours(caffeine_mg):
    if caffeine_mg <= 0:
        return 0

    effect_hours = BASE_EFFECT_HOURS + (caffeine_mg / REFERENCE_CAFFEINE_MG) * 1.2
    return min(effect_hours, MAX_EFFECT_HOURS)


def format_hours(hours):
    total_minutes = int(round(hours * 60))
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h} h {m} min"


def get_risk_level(mg_per_kg):
    if mg_per_kg < 1:
        return "Low", "Your caffeine dose is low for your body weight."
    elif mg_per_kg < 3:
        return "Moderate", "Your caffeine dose is moderate for your body weight."
    else:
        return "High", "This is a high caffeine dose for your body weight."