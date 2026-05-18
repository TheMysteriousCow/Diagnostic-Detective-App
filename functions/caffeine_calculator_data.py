import os
import json
import time

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from utils.data_manager import DataManager

from functions.caffeine_calculator_math import (
    PEAK_MINUTES,
    CRASH_HOURS,
    RECOVERY_HOURS,
    search_matches,
    caffeine_effect_duration_hours,
    format_hours,
    get_risk_level,
    reset_caffeine_session_after_clear,
)


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


def get_username():
    return st.session_state.get("username", "default_user")


def get_data_file():
    return f"data_{get_username()}.csv"


def get_current_file():
    return f"current_caffeine_{get_username()}.json"


def empty_current_data():
    return {
        "entries": [],
        "countdown_end_time": None,
        "countdown_total_seconds": 0,
        "last_drink": None,
    }


def load_history():
    return data_manager.load_user_data(
        get_data_file(),
        initial_value=pd.DataFrame(columns=[
            "timestamp",
            "Drink",
            "Caffeine (mg)",
            "Volume (ml)"
        ])
    )


def save_history(df):
    data_manager.save_user_data(df, get_data_file())


def load_current():
    data = data_manager.load_user_data(
        get_current_file(),
        initial_value=empty_current_data()
    )

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            return empty_current_data()

    if not isinstance(data, dict):
        return empty_current_data()

    if "entries" not in data:
        data["entries"] = []

    return data


def save_current(data):
    data_manager.save_user_data(data, get_current_file())


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


def render_header():
    st.markdown("<div class='main-title'>Caffeine Calculator</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Choose your drink and calculate your caffeine intake.</div>",
        unsafe_allow_html=True
    )


def render_drink_selector():
    st.markdown("<div class='section-title'>Choose your Drink</div>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 4, 1])

    with center:
        st.markdown("### Select date and time")

        date_col, time_col = st.columns(2)

        with date_col:
            st.date_input("Date", key="intake_date")

        with time_col:
            st.time_input("Time", key="intake_time", step=60)

        selected_datetime = pd.Timestamp.combine(
            st.session_state.intake_date,
            st.session_state.intake_time
        )

        selected_timestamp = pd.Timestamp(selected_datetime)
        selected_unix_time = int(selected_timestamp.timestamp())

        search_text = st.text_input(
            "Search drink",
            placeholder="Example: redbull, latte machiato, coffe..."
        )

        filtered_drinks = {
            name: info
            for name, info in DRINKS.items()
            if search_matches(search_text, name)
        }

        if len(filtered_drinks) == 0:
            st.info("No drink found. Try another spelling.")

        drink_items = list(filtered_drinks.items())

        for i in range(0, len(drink_items), 3):
            cols = st.columns(3)

            for col, item in zip(cols, drink_items[i:i + 3]):
                drink_name, info = item

                with col:
                    st.markdown("<div class='drink-card'>", unsafe_allow_html=True)

                    drink_image_path = os.path.join("images", info["image"])

                    if os.path.exists(drink_image_path):
                        st.image(drink_image_path, use_container_width=True)
                    else:
                        st.write("🥤")

                    if st.button(drink_name, key=f"drink_{drink_name}", use_container_width=True):
                        current_data = add_drink_to_current(
                            drink_name,
                            info,
                            selected_datetime,
                            selected_unix_time
                        )

                        last_entry = current_data.get("last_drink", {})

                        st.session_state.current_data = current_data
                        st.session_state.selected_drink = last_entry.get("Drink")
                        st.session_state.selected_caffeine_mg = last_entry.get("Caffeine (mg)", 0)
                        st.session_state.selected_volume_ml = last_entry.get("Volume (ml)", 0)
                        st.session_state.drink_start_time = last_entry.get("start_time")
                        st.session_state.countdown_end_time = current_data.get("countdown_end_time")
                        st.session_state.countdown_total_seconds = current_data.get("countdown_total_seconds", 0)
                        st.session_state.scroll_to_timeline = True
                        st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)


def render_caffeine_timeline():
    current_data, current_entries, current_df, current_total = get_current_summary()

    now = int(time.time())
    end_time = current_data.get("countdown_end_time")
    has_active_current_entries = bool(current_entries) and end_time and end_time > now

    if not has_active_current_entries:
        return

    st.markdown("<div id='caffeine-timeline'></div>", unsafe_allow_html=True)

    if st.session_state.scroll_to_timeline:
        components.html("""
        <script>
            const timeline = window.parent.document.querySelector('#caffeine-timeline');
            if (timeline) {
                timeline.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        </script>
        """, height=0)

        st.session_state.scroll_to_timeline = False

    last_drink = current_data.get("last_drink", {})
    selected_drink = last_drink.get("Drink", "Selected drink")
    caffeine_mg = last_drink.get("Caffeine (mg)", 0)
    volume_ml = last_drink.get("Volume (ml)", 0)

    total_seconds = max(current_data.get("countdown_total_seconds", 1), 1)
    effect_hours = caffeine_effect_duration_hours(caffeine_mg)

    saved_timestamp = last_drink.get("timestamp", "")
    saved_timestamp_display = pd.to_datetime(saved_timestamp, errors="coerce")

    st.success(f"You selected: **{selected_drink}**")

    if not pd.isna(saved_timestamp_display):
        st.write(f"Saved date and time: **{saved_timestamp_display.strftime('%d.%m.%Y %H:%M')}**")

    st.markdown("### Caffeine Timeline")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Peak", f"{PEAK_MINUTES} min", "about 0 h 45 min")

    with col2:
        st.metric("Crash", f"{CRASH_HOURS} h", f"{CRASH_HOURS * 60} min")

    with col3:
        st.metric("Recovery", f"{RECOVERY_HOURS} h", f"{RECOVERY_HOURS * 60} min")

    with col4:
        remaining_seconds = max(end_time - now, 0)
        remaining_hours = remaining_seconds / 3600
        st.metric("Remaining effect", format_hours(remaining_hours))

    components.html(build_countdown_html(end_time, total_seconds), height=330)

    st.info(
        f"{selected_drink} contains **{caffeine_mg} mg caffeine** in **{volume_ml} ml**. "
        f"This drink adds about **{format_hours(effect_hours)}** to your caffeine effect countdown."
    )


def render_current_entries():
    current_data, current_entries, current_df, current_total = get_current_summary()

    st.markdown("<div class='clear-card'>", unsafe_allow_html=True)
    st.markdown("<div class='personal-title'>Current Calculator Entries</div>", unsafe_allow_html=True)

    if current_entries:
        st.metric("Current caffeine in calculator", f"{current_total:.0f} mg")

        if st.button("Clear current calculator entries", use_container_width=True):
            reset_caffeine_session_after_clear()
            st.session_state.current_data = clear_current()
            st.rerun()
    else:
        st.info("No current calculator entries. The countdown is empty.")

    st.markdown("</div>", unsafe_allow_html=True)


def render_personal_impact(profile_weight, profile_height):
    current_data, current_entries, current_df, current_total = get_current_summary()

    st.markdown("<div class='personal-card'>", unsafe_allow_html=True)
    st.markdown("<div class='personal-title'>Personalized Caffeine Impact</div>", unsafe_allow_html=True)

    if profile_weight and profile_weight > 0:
        mg_per_kg = current_total / profile_weight
        personal_daily_limit = profile_weight * 3
        daily_percentage = min((current_total / personal_daily_limit) * 100, 999)

        risk_level, risk_text = get_risk_level(mg_per_kg)

        pcol1, pcol2, pcol3, pcol4 = st.columns(4)

        with pcol1:
            st.metric("Body weight", f"{profile_weight:g} kg")

        with pcol2:
            st.metric("Dose per kg current", f"{mg_per_kg:.2f} mg/kg")

        with pcol3:
            st.metric("Current intake", f"{current_total:.0f} mg")

        with pcol4:
            st.metric("Personal daily guide", f"{personal_daily_limit:.0f} mg")

        st.progress(min(daily_percentage / 100, 1.0))

        st.write(
            f"You have used **{daily_percentage:.0f}%** "
            f"of your personal caffeine guide in the current calculator."
        )

        if risk_level == "Low":
            st.success(f"Risk level: {risk_level} — {risk_text}")
        elif risk_level == "Moderate":
            st.warning(f"Risk level: {risk_level} — {risk_text}")
        else:
            st.error(f"Risk level: {risk_level} — {risk_text}")

        if profile_height and profile_height > 0:
            bmi = profile_weight / (profile_height ** 2)
            st.caption(
                f"Your saved height is {profile_height:g} m. Your BMI is approximately {bmi:.1f}. "
                f"Height is shown for profile context, but caffeine impact is mainly calculated using body weight."
            )

    else:
        st.warning(
            "No valid weight found in your profile. Please enter your weight in Your Profile "
            "to get a personalized caffeine calculation."
        )

    st.markdown("</div>", unsafe_allow_html=True)


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