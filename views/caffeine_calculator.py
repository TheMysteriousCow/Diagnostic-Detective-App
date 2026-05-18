import os
import time
from datetime import datetime

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from utils.profile_utils import load_profile
from functions.logo import set_logo

from functions.caffeine_calculator_data import (
    DRINKS,
    load_history,
    load_current,
    clear_current,
    get_current_summary,
    add_drink_to_current,
    get_page_css,
    build_countdown_html,
)

from functions.caffeine_calculator_math import (
    PEAK_MINUTES,
    CRASH_HOURS,
    RECOVERY_HOURS,
    safe_float,
    search_matches,
    caffeine_effect_duration_hours,
    format_hours,
    get_risk_level,
)


st.set_page_config(page_title="Caffeine Calculator", layout="wide")

username = st.session_state.get("username")

if username is None:
    st.error("No user logged in.")
    st.stop()

profile = load_profile(username)
profile_weight = safe_float(profile.get("weight", ""))
profile_height = safe_float(profile.get("height", ""))

image_path = os.path.join(os.getcwd(), "images", "logo.png")

set_logo(
    image_path,
    top=-40,
    right=-20,
    width=140
)

st.markdown(get_page_css(), unsafe_allow_html=True)

st.markdown("<div class='main-title'>Caffeine Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Choose your drink and calculate your caffeine intake.</div>", unsafe_allow_html=True)


if "selected_drink" not in st.session_state:
    st.session_state.selected_drink = None

if "selected_caffeine_mg" not in st.session_state:
    st.session_state.selected_caffeine_mg = 0

if "selected_volume_ml" not in st.session_state:
    st.session_state.selected_volume_ml = 0

if "drink_start_time" not in st.session_state:
    st.session_state.drink_start_time = None

if "countdown_end_time" not in st.session_state:
    st.session_state.countdown_end_time = None

if "countdown_total_seconds" not in st.session_state:
    st.session_state.countdown_total_seconds = 0

if "scroll_to_timeline" not in st.session_state:
    st.session_state.scroll_to_timeline = False

if "data_df" not in st.session_state:
    st.session_state["data_df"] = load_history()

if "current_data" not in st.session_state:
    st.session_state.current_data = load_current()

if "intake_date" not in st.session_state:
    st.session_state.intake_date = datetime.now().date()

if "intake_time" not in st.session_state:
    st.session_state.intake_time = datetime.now().time().replace(microsecond=0)


current_data = load_current()
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


st.markdown("<div class='section-title'>Choose your Drink</div>", unsafe_allow_html=True)

left, center, right = st.columns([1, 4, 1])

with center:
    st.markdown("### Select date and time")

    date_col, time_col = st.columns(2)

    with date_col:
        st.date_input("Date", key="intake_date")

    with time_col:
        st.time_input("Time", key="intake_time", step=60)

    selected_datetime = datetime.combine(
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


current_data, current_entries, current_df, current_total = get_current_summary()

now = int(time.time())
end_time = current_data.get("countdown_end_time")
has_active_current_entries = bool(current_entries) and end_time and end_time > now

if has_active_current_entries:
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


st.markdown("<div class='clear-card'>", unsafe_allow_html=True)
st.markdown("<div class='personal-title'>Current Calculator Entries</div>", unsafe_allow_html=True)

if current_entries:
    st.metric("Current caffeine in calculator", f"{current_total:.0f} mg")

    if st.button("Clear current calculator entries", use_container_width=True):
        st.session_state.current_data = clear_current()
        st.session_state.selected_drink = None
        st.session_state.selected_caffeine_mg = 0
        st.session_state.selected_volume_ml = 0
        st.session_state.drink_start_time = None
        st.session_state.countdown_end_time = None
        st.session_state.countdown_total_seconds = 0
        st.session_state.scroll_to_timeline = False
        st.rerun()
else:
    st.info("No current calculator entries. The countdown is empty.")

st.markdown("</div>", unsafe_allow_html=True)


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

    st.write(f"You have used **{daily_percentage:.0f}%** of your personal caffeine guide in the current calculator.")

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