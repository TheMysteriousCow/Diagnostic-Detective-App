import html
import pandas as pd
import streamlit as st
from datetime import datetime


DIARY_FILE = "diary.csv"


def empty_diary_df():
    return pd.DataFrame(columns=[
        "timestamp",
        "Diary Entry"
    ])


def render_diary(data_manager, diary_title):
    st.markdown(f"<div class='section-title'>{diary_title}</div>", unsafe_allow_html=True)

    if "diary_df" not in st.session_state:
        st.session_state["diary_df"] = data_manager.load_user_data(
            DIARY_FILE,
            initial_value=empty_diary_df()
        )

    if st.session_state["diary_df"] is None:
        st.session_state["diary_df"] = empty_diary_df()

    col_date, col_time = st.columns(2)

    with col_date:
        diary_date = st.date_input(
            "Choose a date:",
            value=datetime.now().date()
        )

    with col_time:
        diary_time = st.time_input(
            "Choose a time:",
            value=datetime.now().time().replace(second=0, microsecond=0),
            step=60
        )

    diary_timestamp = datetime.combine(diary_date, diary_time)

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
                "timestamp": diary_timestamp,
                "Diary Entry": diary_text.strip()
            }])

            st.session_state["diary_df"] = pd.concat(
                [st.session_state["diary_df"], new_entry],
                ignore_index=True
            )

            data_manager.save_user_data(
                st.session_state["diary_df"],
                DIARY_FILE
            )

            st.success("Diary entry saved!")
            st.rerun()

    diary_df = st.session_state["diary_df"]

    if not diary_df.empty:
        diary_df["timestamp"] = pd.to_datetime(diary_df["timestamp"], errors="coerce")
        diary_df = diary_df.dropna(subset=["timestamp"])
        diary_df = diary_df.sort_values("timestamp", ascending=False).reset_index(drop=True)
        st.session_state["diary_df"] = diary_df

        st.markdown("<div class='section-title'>Saved Diary Entries</div>", unsafe_allow_html=True)

        for index, row in diary_df.iterrows():
            date_time = row["timestamp"].strftime("%d.%m.%Y %H:%M")
            entry = html.escape(str(row["Diary Entry"])).replace("\n", "<br>")

            st.markdown(f"""
            <div class="diary-card">
                <strong>{date_time}</strong><br><br>
                {entry}
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Delete Entry", key=f"delete_diary_{index}"):
                st.session_state["diary_df"] = diary_df.drop(index).reset_index(drop=True)

                data_manager.save_user_data(
                    st.session_state["diary_df"],
                    DIARY_FILE
                )

                st.success("Diary entry deleted!")
                st.rerun()
    else:
        st.info("No diary entries yet.")