import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError

from utils.data_manager import DataManager
from utils.login_manager import LoginManager


data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="diagnosticdetective"
)

st.session_state["data_manager"] = data_manager

login_manager = LoginManager(data_manager)
login_manager.login_register()

if 'data_df' not in st.session_state:
    try:
        df = data_manager.load_user_data(
            'data.csv',
            initial_value=pd.DataFrame()
        )
    except EmptyDataError:
        df = pd.DataFrame()

    if not df.empty:
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    st.session_state['data_df'] = df


# SIDEBAR FARBEN
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #f3f4f6;
}

/* Alle Navigationseinträge etwas runder machen */
section[data-testid="stSidebar"] a {
    border-radius: 10px;
    padding: 8px 12px !important;
    margin-bottom: 6px;
    display: block;
    color: black !important;
    text-decoration: none !important;
}

/* Your Profile – Pastell orange */
section[data-testid="stSidebar"] a[href*="your_profile"] {
    background-color: #FFD8B1 !important;
}

/* Additional Data – Pastell grün */
section[data-testid="stSidebar"] a[href*="additional_data"] {
    background-color: #FFE5B4 !important;
}

/* Home – hellrot */
section[data-testid="stSidebar"] a[href*="home1"],
section[data-testid="stSidebar"] a[href*="home.py"] {
    background-color: #F7C6C7 !important;
}

/* Koffein Rechner – mitteldunkelrosa */
section[data-testid="stSidebar"] a[href*="caffeine_calculator"] {
    background-color: #E7A8C9 !important;
}

/* Statistik – pastellrosa */
section[data-testid="stSidebar"] a[href*="statistic"] {
    background-color: #F8D6E6 !important;
}

/* Recommendations – pastellgelb */
section[data-testid="stSidebar"] a[href*="recommendations"] {
    background-color: #FFF4B8 !important;
}

/* Alternatives – pastellblau */
section[data-testid="stSidebar"] a[href*="alternatives"] {
    background-color: #CFE8FF !important;
}

/* optional: Hover */
section[data-testid="stSidebar"] a:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)


home = st.Page("views/home.py", title="Home", icon="🏠")
your_profile = st.Page("views/your_profile.py", title="Your Profile", icon="☕")
additional_data = st.Page("views/additional_data.py", title="Additional Data", icon="☕")
home1 = st.Page("views/home1.py", title="Home", icon="☕")
calculator = st.Page("views/caffeine_calculator.py", title="Caffeine Calculator", icon="☕")
statistics = st.Page("views/statistic.py", title="History", icon="☕")
recommendations = st.Page("views/recommendations.py", title="Recommendations", icon="☕")
alternatives = st.Page("views/alternatives.py", title="Alternatives", icon="☕")

pg = st.navigation([home, your_profile, additional_data, home1, calculator, statistics, recommendations, alternatives])
pg.run()