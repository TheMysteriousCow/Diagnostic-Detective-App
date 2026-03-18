import pandas as pd
import streamlit as st
import os
from datetime import datetime, date

from functions.caffeine_math import caffeine_remaining

st.title("☕ Koffeinabbau-Rechner")
st.image(os.path.join(os.path.dirname(__file__), "titelbild.png"), use_container_width=True)

if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

HALF_LIFE = 5.0

st.caption("Für alle Berechnungen wird eine feste Halbwertszeit von 5 Stunden verwendet.")

with st.form("caffeine_form"):

    drink = st.selectbox(
        "Getränk",
        ["Kaffee", "Espresso", "Energy Drink", "Red Bull", "NOCCO", "Mate", "Matcha", "Schwarzer Tee", "Eigener Wert"]
    )

    default_values = {
        "Kaffee": 95,
        "Espresso": 60,
        "Energy Drink": 80,
        "Red Bull": 80,
        "NOCCO": 180,
        "Mate": 80,
        "Matcha": 70,
        "Schwarzer Tee": 45,
        "Eigener Wert": 0
    }

    col1, col2 = st.columns(2)

    with col1:
        caffeine_per_ml = st.number_input(
            "Koffein pro ml (mg/ml)",
            min_value=0.0,
            max_value=50.0,
            value=float(default_values[drink] / 250 if drink != "Eigener Wert" else 0.0),
            step=0.1
        )

    with col2:
        volume_ml = st.number_input(
            "Getränkemenge (ml)",
            min_value=1.0,
            max_value=1000.0,
            value=250.0,
            step=10.0
        )

    dose_mg = caffeine_per_ml * volume_ml

    intake_time = st.time_input(
        "Uhrzeit der Einnahme",
        value=datetime.now().time().replace(second=0, microsecond=0)
    )

    horizon = st.slider(
        "Berechnungszeitraum (Stunden)",
        min_value=6,
        max_value=48,
        value=24
    )

    submit = st.form_submit_button("Ausrechnen")


if submit:
    now = datetime.now()
    taken_at = datetime.combine(date.today(), intake_time)

    hours_since = (now - taken_at).total_seconds() / 3600

    if hours_since < 0:
        hours_since = 0

    current = caffeine_remaining(dose_mg, hours_since, HALF_LIFE)

    caffeine_zero_time = None
    for h in range(1, horizon + 1):
        if caffeine_remaining(dose_mg, h, HALF_LIFE) < 0.5:
            caffeine_zero_time = h
            break

    st.metric("Koffein aktuell im Körper (mg)", f"{current:.1f}")
    st.info(f"Verwendete Halbwertszeit: {HALF_LIFE:.1f} Stunden")

    if caffeine_zero_time:
        st.success(f"✅ Koffein ist nach ca. {caffeine_zero_time} Stunde(n) aus dem Körper")
    else:
        st.warning(f"Innerhalb von {horizon} Stunden ist noch Restkoffein vorhanden")

    data = []
    for h in range(horizon + 1):
        remaining = caffeine_remaining(dose_mg, h, HALF_LIFE)
        data.append({
            "Stunden": h,
            "Koffein (mg)": remaining
        })

    df_chart = pd.DataFrame(data).set_index("Stunden")
    st.line_chart(df_chart)

    if caffeine_zero_time is not None:
        zero_datetime = taken_at + pd.Timedelta(hours=caffeine_zero_time)
        kein_koffein_text = f"nach {caffeine_zero_time} Stunde(n), um {zero_datetime.strftime('%H:%M')} Uhr"
    else:
        kein_koffein_text = f"nicht innerhalb von {horizon} Stunden"

    new_row = {
        "timestamp": now, 
        "Getränk": drink,
        "Wann eingenommen": taken_at.strftime("%d.%m.%Y %H:%M"),
        "Koffeinmenge zu Beginn (mg)": round(dose_mg, 1),
        "Halbwertszeit (h)": HALF_LIFE,
        "Kein Koffein mehr": kein_koffein_text
    }

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], pd.DataFrame([new_row])],
        ignore_index=True
    )

    data_manager = st.session_state["data_manager"]
    data_manager.save_user_data(st.session_state["data_df"], 'data.csv')

st.subheader("Verlauf der Getränke")
st.dataframe(st.session_state["data_df"])