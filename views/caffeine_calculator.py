import pandas as pd
import streamlit as st
import os
from datetime import datetime, date, timedelta

from functions.caffeine_math import caffeine_remaining


# -----------------------------
# PAGE TITLE / IMAGE
# -----------------------------
st.title("☕ Koffeinabbau-Rechner")
st.image(
    os.path.join(os.path.dirname(__file__), "titelbild.png"),
    use_container_width=True
)


# -----------------------------
# SESSION STATE
# -----------------------------
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()


# -----------------------------
# CONSTANTS
# -----------------------------
HALF_LIFE = 5.0

st.caption("Für alle Berechnungen wird eine feste Halbwertszeit von 5 Stunden verwendet.")


# -----------------------------
# INPUT FORM
# -----------------------------
with st.form("caffeine_form"):

    drink = st.selectbox(
        "Getränk",
        [
            "Kaffee",
            "Espresso",
            "Energy Drink",
            "Red Bull",
            "NOCCO",
            "Mate",
            "Matcha",
            "Schwarzer Tee",
            "Eigener Wert"
        ]
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


# -----------------------------
# CALCULATION
# -----------------------------
if submit:
    now = datetime.now()
    taken_at = datetime.combine(date.today(), intake_time)

    # Falls die eingegebene Zeit in der Zukunft liegt,
    # nehmen wir an, das Getränk wurde gestern getrunken.
    if taken_at > now:
        taken_at = taken_at - timedelta(days=1)

    hours_since = (now - taken_at).total_seconds() / 3600
    hours_since = max(0.0, hours_since)

    current = caffeine_remaining(dose_mg, hours_since, HALF_LIFE)
    remaining_after_24h = caffeine_remaining(dose_mg, 24, HALF_LIFE)
    remaining_after_horizon = caffeine_remaining(dose_mg, horizon, HALF_LIFE)

    caffeine_zero_time = None
    for h in range(1, horizon + 1):
        if caffeine_remaining(dose_mg, h, HALF_LIFE) < 0.5:
            caffeine_zero_time = h
            break

    # -----------------------------
    # METRICS / INFO
    # -----------------------------
    st.metric("Koffein aktuell im Körper (mg)", f"{current:.1f}")
    st.metric(f"Koffein nach {horizon} Stunde(n)", f"{remaining_after_horizon:.1f} mg")
    st.info(f"Verwendete Halbwertszeit: {HALF_LIFE:.1f} Stunden")

    if caffeine_zero_time is not None:
        st.success(f"✅ Koffein ist nach ca. {caffeine_zero_time} Stunde(n) aus dem Körper")
    else:
        st.warning(f"Innerhalb von {horizon} Stunden ist noch Restkoffein vorhanden")

    # -----------------------------
    # CHART DATA
    # -----------------------------
    data = []
    for h in range(horizon + 1):
        remaining = caffeine_remaining(dose_mg, h, HALF_LIFE)
        data.append({
            "Stunden": h,
            "Koffein (mg)": round(remaining, 1)
        })

    df_chart = pd.DataFrame(data).set_index("Stunden")
    st.line_chart(df_chart)

    st.subheader("Koffeinverlauf pro Stunde")
    st.dataframe(pd.DataFrame(data), use_container_width=True)

    # -----------------------------
    # SAVE RESULT IN SESSION STATE
    # -----------------------------
    new_row = {
        "timestamp": now,
        "Einnahmezeitpunkt": taken_at,
        "Getränk": drink,
        "Menge (ml)": round(volume_ml, 1),
        "Koffein pro ml (mg/ml)": round(caffeine_per_ml, 2),
        "Berechnungszeitraum (h)": horizon,
        "Koffeinmenge zu Beginn (mg)": round(dose_mg, 1),
        "Aktuell im Körper (mg)": round(current, 1),
        "Koffeinmenge nach 24 h (mg)": round(remaining_after_24h, 1),
        f"Koffeinmenge nach {horizon} h (mg)": round(remaining_after_horizon, 1)
    }

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], pd.DataFrame([new_row])],
        ignore_index=True
    )

    cols = st.session_state["data_df"].columns.tolist()
    if "timestamp" in cols:
        cols = ["timestamp"] + [col for col in cols if col != "timestamp"]
        st.session_state["data_df"] = st.session_state["data_df"][cols]

    # -----------------------------
    # OPTIONAL SAVE TO DATA MANAGER
    # -----------------------------
    if "data_manager" in st.session_state:
        try:
            data_manager = st.session_state["data_manager"]
            data_manager.save_user_data(st.session_state["data_df"], "data.csv")
        except Exception as e:
            st.warning(f"Speichern über data_manager nicht möglich: {e}")
    else:
        st.info("Die Daten wurden nur für diese Session gespeichert.")