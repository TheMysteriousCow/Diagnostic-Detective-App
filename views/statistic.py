import pandas as pd
import streamlit as st
from datetime import datetime

# -------------------------------------------------
# CSS
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: white;
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #5C4033 !important;
}

.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

.section-title {
    font-size: 1.8rem;
    font-family: 'Georgia', serif;
    font-weight: 600;
    color: #5C4033;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

div.stButton > button {
    background-color: #CDECCF;
    color: #5C4033;
    border: none;
    border-radius: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.markdown("<div class='main-title'>History</div>", unsafe_allow_html=True)

# -------------------------------------------------
# HISTORY DATA
# -------------------------------------------------
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=[
        "timestamp",
        "Drink",
        "Caffeine (mg)"
    ])

data_df = st.session_state["data_df"]

if not data_df.empty and "timestamp" in data_df.columns:
    data_df["timestamp"] = pd.to_datetime(data_df["timestamp"], errors="coerce")
    data_df = data_df.sort_values("timestamp", ascending=False)
    st.session_state["data_df"] = data_df

st.markdown("<div class='section-title'>Drink History</div>", unsafe_allow_html=True)

if data_df.empty:
    st.info("No data available yet. Please choose a drink in the Caffeine Calculator first.")
else:
    display_df = data_df.copy()

    if "timestamp" in display_df.columns:
        display_df["Date"] = display_df["timestamp"].dt.strftime("%d.%m.%Y")
        display_df["Time"] = display_df["timestamp"].dt.strftime("%H:%M")

    columns_to_show = ["Date", "Time", "Drink", "Caffeine (mg)"]
    existing_columns = [col for col in columns_to_show if col in display_df.columns]

    st.dataframe(display_df[existing_columns], use_container_width=True)

# -------------------------------------------------
# DELETE HISTORY
# -------------------------------------------------
if st.button("🗑️ Clear History"):
    st.session_state["data_df"] = pd.DataFrame(columns=[
        "timestamp",
        "Drink",
        "Caffeine (mg)"
    ])

    if "data_manager" in st.session_state:
        data_manager = st.session_state["data_manager"]
        data_manager.save_user_data(st.session_state["data_df"], "data.csv")

    st.success("History has been cleared!")
    st.rerun()

# -------------------------------------------------
# MY DIARY
# -------------------------------------------------
st.markdown("<div class='section-title'>My caffeine diary</div>", unsafe_allow_html=True)

if "diary_df" not in st.session_state:
    st.session_state["diary_df"] = pd.DataFrame(columns=[
        "timestamp",
        "Diary Entry"
    ])

diary_text = st.text_area(
    "Write your diary entry here:",
    height=180,
    placeholder="How do you feel today? Did caffeine affect your energy, sleep, mood or concentration?"
)

if st.button("💾 Save Diary Entry"):
    if diary_text.strip() == "":
        st.warning("Please write something before saving.")
    else:
        new_entry = pd.DataFrame([{
            "timestamp": datetime.now(),
            "Diary Entry": diary_text.strip()
        }])

        st.session_state["diary_df"] = pd.concat(
            [st.session_state["diary_df"], new_entry],
            ignore_index=True
        )

        if "data_manager" in st.session_state:
            data_manager = st.session_state["data_manager"]
            data_manager.save_user_data(st.session_state["diary_df"], "diary.csv")

        st.success("Diary entry saved!")
        st.rerun()

# -------------------------------------------------
# SHOW DIARY ENTRIES
# -------------------------------------------------
diary_df = st.session_state["diary_df"]

if not diary_df.empty:
    diary_df["timestamp"] = pd.to_datetime(diary_df["timestamp"], errors="coerce")
    diary_df = diary_df.sort_values("timestamp", ascending=False)

    st.markdown("<div class='section-title'>Saved Diary Entries</div>", unsafe_allow_html=True)

    for _, row in diary_df.iterrows():
        date_time = row["timestamp"].strftime("%d.%m.%Y %H:%M")
        entry = row["Diary Entry"]

        st.markdown(f"""
        <div style="
            border: 2px solid #CDECCF;
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 14px;
            background-color: #FAFFFA;
        ">
            <strong>{date_time}</strong><br><br>
            {entry}
        </div>
        """, unsafe_allow_html=True)