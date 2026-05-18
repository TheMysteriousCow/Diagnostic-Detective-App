import re
import time
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher

import streamlit as st


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


def initialize_caffeine_session(load_history_func, load_current_func):
    defaults = {
        "selected_drink": None,
        "selected_caffeine_mg": 0,
        "selected_volume_ml": 0,
        "drink_start_time": None,
        "countdown_end_time": None,
        "countdown_total_seconds": 0,
        "scroll_to_timeline": False,
        "intake_date": datetime.now().date(),
        "intake_time": datetime.now().time().replace(microsecond=0),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "data_df" not in st.session_state:
        st.session_state["data_df"] = load_history_func()

    if "current_data" not in st.session_state:
        st.session_state.current_data = load_current_func()


def restore_active_countdown_to_session(load_current_func):
    current_data = load_current_func()
    current_entries = current_data.get("entries", [])
    last_drink = current_data.get("last_drink")

    now_check = int(time.time())
    current_end_time = current_data.get("countdown_end_time")

    if current_entries and current_end_time and current_end_time > now_check:
        st.session_state.countdown_end_time = current_end_time
        st.session_state.countdown_total_seconds = current_data.get("countdown_total_seconds", 0)

        if last_drink:
            st.session_state.selected_drink = last_drink.get("Drink")
            st.session_state.selected_caffeine_mg = last_drink.get("Caffeine (mg)", 0)
            st.session_state.selected_volume_ml = last_drink.get("Volume (ml)", 0)
            st.session_state.drink_start_time = last_drink.get("start_time", now_check)


def reset_caffeine_session_after_clear():
    st.session_state.current_data = None
    st.session_state.selected_drink = None
    st.session_state.selected_caffeine_mg = 0
    st.session_state.selected_volume_ml = 0
    st.session_state.drink_start_time = None
    st.session_state.countdown_end_time = None
    st.session_state.countdown_total_seconds = 0
    st.session_state.scroll_to_timeline = False