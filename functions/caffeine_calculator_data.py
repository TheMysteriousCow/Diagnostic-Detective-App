import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from functions.caffeine_calculator_math import caffeine_effect_duration_hours


username = st.session_state.get("username", "default_user")
DATA_FILE = f"data_{username}.csv"
CURRENT_FILE = f"current_caffeine_{username}.json"

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="caffeine_calculator_app"
)

DRINKS = {
    "Red Bull": {"image": "Redbull.png", "caffeine_mg": 114, "volume_ml": 355},
    "Monster": {"image": "Monster.png", "caffeine_mg": 160, "volume_ml": 500},
    "El Tony Mate Zero": {"image": "ElTonyMateZero.png", "caffeine_mg": 85.8, "volume_ml": 330},
    "El Tony Mate": {"image": "ElTonyMate.png", "caffeine_mg": 76, "volume_ml": 330},
    "Mate Bio Puro": {"image": "MateBioPuro.png", "caffeine_mg": 80, "volume_ml": 500},
    "Nocco": {"image": "Nocco.png", "caffeine_mg": 180, "volume_ml": 330},
    "Matcha": {"image": "Matcha.png", "caffeine_mg": 79, "volume_ml": 250},
    "Espresso": {"image": "Espresso.png", "caffeine_mg": 60, "volume_ml": 30},
    "Doppio": {"image": "Doppio.png", "caffeine_mg": 120, "volume_ml": 60},
    "Cappuccino": {"image": "Cappuccino.png", "caffeine_mg": 60, "volume_ml": 180},
    "Latte Macchiato": {"image": "LatteMacchiato.png", "caffeine_mg": 60, "volume_ml": 250},
    "Flat White": {"image": "FlatWhite.png", "caffeine_mg": 120, "volume_ml": 160},
    "Café Crème": {"image": "CaféCrème.png", "caffeine_mg": 90, "volume_ml": 180},
    "Filterkaffee": {"image": "Filterkaffee.png", "caffeine_mg": 100, "volume_ml": 200},
    "Cold Brew": {"image": "ColdBrew.png", "caffeine_mg": 140, "volume_ml": 250},
}


def empty_current_data():
    return {
        "entries": [],
        "countdown_end_time": None,
        "countdown_total_seconds": 0,
        "last_drink": None,
    }


def load_history():
    return data_manager.load_user_data(
        DATA_FILE,
        initial_value=pd.DataFrame(columns=[
            "timestamp",
            "Drink",
            "Caffeine (mg)",
            "Volume (ml)"
        ])
    )


def save_history(df):
    data_manager.save_user_data(df, DATA_FILE)


def load_current():
    data = data_manager.load_user_data(
        CURRENT_FILE,
        initial_value=empty_current_data()
    )

    if isinstance(data, str):
        try:
            import json
            data = json.loads(data)
        except:
            return empty_current_data()

    if not isinstance(data, dict):
        return empty_current_data()

    return data


def save_current(data):
    data_manager.save_user_data(data, CURRENT_FILE)


def clear_current():
    data = empty_current_data()
    save_current(data)
    return data


def get_current_summary():
    current_data = load_current()
    entries = current_data.get("entries", [])

    if entries:
        current_df = pd.DataFrame(entries)
        total = current_df["Caffeine (mg)"].sum()
    else:
        current_df = pd.DataFrame(columns=[
            "timestamp",
            "Drink",
            "Caffeine (mg)",
            "Volume (ml)"
        ])
        total = 0

    return current_data, entries, current_df, total


def add_drink_to_current(drink_name, drink_info, selected_datetime, selected_unix_time):
    caffeine_mg = drink_info["caffeine_mg"]
    volume_ml = drink_info["volume_ml"]

    effect_hours = caffeine_effect_duration_hours(caffeine_mg)
    effect_seconds = int(effect_hours * 3600)

    current_data = load_current()
    current_end_time = current_data.get("countdown_end_time")

    if current_end_time and current_end_time > selected_unix_time:
        new_end_time = current_end_time + effect_seconds
    else:
        new_end_time = selected_unix_time + effect_seconds

    selected_timestamp = pd.Timestamp(selected_datetime)

    entry = {
        "timestamp": selected_timestamp.isoformat(),
        "Drink": drink_name,
        "Caffeine (mg)": caffeine_mg,
        "Volume (ml)": volume_ml,
        "effect_seconds": effect_seconds,
        "start_time": selected_unix_time,
    }

    current_data["entries"].append(entry)
    current_data["countdown_end_time"] = new_end_time
    current_data["countdown_total_seconds"] = max(new_end_time - selected_unix_time, 1)
    current_data["last_drink"] = entry

    save_current(current_data)

    history_df = load_history()

    history_entry = pd.DataFrame([{
        "timestamp": selected_timestamp,
        "Drink": drink_name,
        "Caffeine (mg)": caffeine_mg,
        "Volume (ml)": volume_ml,
    }])

    history_df = pd.concat([history_df, history_entry], ignore_index=True)
    save_history(history_df)

    return current_data


def get_page_css():
    return """
<style>
.stApp {
    background-color: white;
    color: #5C4033 !important;
}

html, body, p, div, span, label, input, textarea,
h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, .stCaption,
[data-testid="stMarkdownContainer"],
[data-testid="stText"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    color: #5C4033 !important;
}

input {
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

input::placeholder {
    color: #8B6F63 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

div[data-baseweb="input"],
div[data-baseweb="select"] {
    background-color: #EDEFF2 !important;
    border-radius: 14px !important;
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #EDEFF2 !important;
    border-radius: 14px !important;
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

div[data-baseweb="input"] input {
    background-color: #EDEFF2 !important;
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

div[data-baseweb="input"] svg,
div[data-baseweb="select"] svg {
    color: #5C4033 !important;
    fill: #5C4033 !important;
}

[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p {
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"],
[data-testid="stTimeInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #EDEFF2 !important;
    border-radius: 14px !important;
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[data-baseweb="calendar"] {
    color: #5C4033 !important;
    font-family: Arial, sans-serif !important;
    font-weight: 400 !important;
}

.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033 !important;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    font-family: Arial, sans-serif;
    color: #5C4033 !important;
    margin-bottom: 2rem;
}

.section-title {
    text-align: center;
    font-size: 1.8rem;
    font-family: 'Georgia', serif;
    font-weight: 600;
    color: #5C4033 !important;
    margin-bottom: 2rem;
}

div.stButton > button {
    width: 100%;
    height: 55px;
    background-color: #CDECCF;
    color: #5C4033 !important;
    border: none;
    border-radius: 16px;
    font-size: 1.1rem;
    font-family: Arial, sans-serif;
    font-weight: 600;
    white-space: nowrap;
}

div.stButton > button:hover {
    background-color: #BEE6C2;
    color: #5C4033 !important;
}

.drink-card {
    margin-bottom: 25px;
}

.personal-card {
    background-color: #f7f4f1;
    border-radius: 24px;
    padding: 28px;
    margin-top: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    color: #5C4033 !important;
}

.personal-title {
    color: #5C4033 !important;
    font-size: 1.6rem;
    font-family: Georgia, serif;
    font-weight: 600;
    text-align: center;
    margin-bottom: 20px;
}

.clear-card {
    background-color: #fff7f2;
    border-radius: 24px;
    padding: 24px;
    margin-top: 10px;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    color: #5C4033 !important;
}
</style>
"""


def build_countdown_html(end_time, total_seconds):
    return f"""
<div style="
    display:flex;
    align-items:center;
    justify-content:center;
    gap:50px;
    margin-top:35px;
    margin-bottom:25px;
    font-family:Arial, sans-serif;
    color:#5C4033;
">
    <div style="
        background:#f7f4f1;
        border-radius:24px;
        padding:28px 36px;
        min-width:300px;
        text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.08);
        color:#5C4033;
    ">
        <div style="color:#5C4033; font-size:1.1rem; margin-bottom:10px;">
            Cumulative caffeine countdown
        </div>

        <div id="countdown" style="
            color:#5C4033;
            font-size:2.4rem;
            font-weight:700;
            letter-spacing:1px;
        ">
            Loading...
        </div>

        <div id="status" style="color:#5C4033; font-size:0.95rem; margin-top:10px;">
            Every added drink extends the remaining caffeine effect.
        </div>
    </div>

    <div style="
        width:120px;
        height:220px;
        border:5px solid #5C4033;
        border-radius:0 0 35px 35px;
        position:relative;
        overflow:hidden;
        background:rgba(255,255,255,0.85);
        box-shadow:0 8px 20px rgba(0,0,0,0.12);
    ">
        <div id="liquid" style="
            position:absolute;
            bottom:0;
            left:0;
            width:100%;
            height:100%;
            background:linear-gradient(180deg, #6b3f22 0%, #3b1f12 100%);
            transition:height 1s linear;
        "></div>

        <div style="
            position:absolute;
            top:20px;
            left:25px;
            width:22px;
            height:150px;
            background:rgba(255,255,255,0.22);
            border-radius:20px;
        "></div>
    </div>
</div>

<script>
    const endTime = {end_time * 1000};
    const totalDuration = {total_seconds * 1000};

    function updateCountdown() {{
        const now = new Date().getTime();
        let remaining = endTime - now;

        if (remaining <= 0) {{
            remaining = 0;
            document.getElementById("countdown").innerHTML = "0 h 0 min 0 s";
            document.getElementById("status").innerHTML = "The main caffeine effect is now likely over.";
            document.getElementById("liquid").style.height = "0%";
            return;
        }}

        const hours = Math.floor(remaining / (1000 * 60 * 60));
        const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((remaining % (1000 * 60)) / 1000);

        document.getElementById("countdown").innerHTML =
            hours + " h " + minutes + " min " + seconds + " s";

        const progress = Math.min(Math.max(1 - remaining / totalDuration, 0), 1);
        const liquidHeight = 100 - (progress * 100);

        document.getElementById("liquid").style.height = liquidHeight + "%";
    }}

    updateCountdown();
    setInterval(updateCountdown, 1000);
</script>
"""