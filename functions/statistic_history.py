import pandas as pd
import streamlit as st


DATA_FILE = "data.csv"


def empty_history_df():
    return pd.DataFrame(columns=[
        "timestamp",
        "Drink",
        "Caffeine (mg)",
        "Volume (ml)"
    ])


def render_drink_history(data_manager):
    st.markdown("<div class='section-title'>Drink History</div>", unsafe_allow_html=True)

    data_df = data_manager.load_user_data(
        DATA_FILE,
        initial_value=empty_history_df()
    )

    if data_df is None:
        data_df = empty_history_df()

    if not data_df.empty and "timestamp" in data_df.columns:
        data_df["timestamp"] = pd.to_datetime(data_df["timestamp"], errors="coerce")
        data_df = data_df.dropna(subset=["timestamp"])
        data_df = data_df.sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.session_state["data_df"] = data_df

    if data_df.empty:
        st.info("No data available yet. Please choose a drink in the Caffeine Calculator first.")
    else:
        display_df = data_df.copy()
        display_df["Date"] = display_df["timestamp"].dt.strftime("%d.%m.%Y")
        display_df["Time"] = display_df["timestamp"].dt.strftime("%H:%M")

        columns_to_show = ["Date", "Time", "Drink", "Caffeine (mg)", "Volume (ml)"]
        existing_columns = [col for col in columns_to_show if col in display_df.columns]

        st.dataframe(
            display_df[existing_columns],
            use_container_width=True,
            hide_index=True
        )

    if st.button("🗑️ Clear History"):
        empty_df = empty_history_df()
        st.session_state["data_df"] = empty_df

        data_manager.save_user_data(empty_df, DATA_FILE)

        st.success("History has been cleared!")
        st.rerun()