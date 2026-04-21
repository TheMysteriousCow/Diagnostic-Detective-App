import pandas as pd
import streamlit as st

# -------------------------------------------------
# CSS (einheitliche Farbe + Titelstil)
# -------------------------------------------------
st.markdown("""
<style>

/* Hintergrund */
.stApp {
    background-color: white;
}

/* Einheitliche Schriftfarbe */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #5C4033 !important;
}

/* TITEL wie auf Hauptscreen */
.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)

# Titel (ersetzt st.title)
st.markdown("<div class='main-title'>History</div>", unsafe_allow_html=True)

# -------------------------------------------------
# REST BLEIBT UNVERÄNDERT
# -------------------------------------------------

if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

data_df = st.session_state["data_df"]

if not data_df.empty and "timestamp" in data_df.columns:
    data_df["timestamp"] = pd.to_datetime(data_df["timestamp"], errors="coerce")
    data_df = data_df.sort_values("timestamp")
    st.session_state["data_df"] = data_df

st.subheader("Verlauf der Getränke")

if data_df.empty:
    st.info("Noch keine Daten vorhanden. Führen Sie zuerst eine Berechnung im Koffein Rechner durch.")
else:
    st.dataframe(data_df, use_container_width=True)

    if "timestamp" in data_df.columns and "Koffeinmenge zu Beginn (mg)" in data_df.columns:
        chart_df = data_df.copy()

        chart_df = chart_df.dropna(subset=["timestamp", "Koffeinmenge zu Beginn (mg)"])
        chart_df = chart_df.set_index("timestamp")

        cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
        last_30_days = chart_df.loc[chart_df.index >= cutoff]

        if not last_30_days.empty:
            st.subheader("Koffeinmenge im letzten Monat")
            st.line_chart(last_30_days["Koffeinmenge zu Beginn (mg)"])
            st.caption("X-Achse: Zeitpunkt im letzten Monat · Y-Achse: Koffeinmenge zu Beginn (mg)")
        else:
            st.info("Keine Daten aus dem letzten Monat vorhanden.")

if st.button("🗑️ Verlauf löschen"):
    st.session_state["data_df"] = pd.DataFrame()
    data_manager = st.session_state["data_manager"]
    data_manager.save_user_data(st.session_state["data_df"], "data.csv")
    st.success("Verlauf wurde gelöscht!")
    