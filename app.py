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

/* Home – orange */
section[data-testid="stSidebar"] a[href*="home1"],
section[data-testid="stSidebar"] a[href*="home.py"] {
    background-color: #FFE5B4 !important;
}

/* Your Profile – pastellgelb */
section[data-testid="stSidebar"] a[href*="your_profile"] {
    background-color: #FFF4B8 !important;
}

/* Additional Data – pastellorange */
section[data-testid="stSidebar"] a[href*="additional_data"] {
    background-color: #FFD8B1 !important;
}

/* Koffein Rechner – hellrot */
section[data-testid="stSidebar"] a[href*="caffeine_calculator"] {
    background-color: #F7C6C7 !important;
}

/* Statistik – mitteldunkelrosa */
section[data-testid="stSidebar"] a[href*="statistic"] {
    background-color: #E7A8C9 !important;
}

/* Recommendations – pastellrosa */
section[data-testid="stSidebar"] a[href*="recommendations"] {
    background-color: #F8D6E6 !important;
}

/* Alternatives – pastellblau */
section[data-testid="stSidebar"] a[href*="alternatives"] {
    background-color: #CFE8FF !important;
}
            
/* Professional Help – mitteldunkles blau */
section[data-testid="stSidebar"] a[href*="professional_help"] {
    background-color: #6FA3CC !important;
}

/* optional: Hover */
section[data-testid="stSidebar"] a:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

home1 = st.Page("views/home1.py", title="Home", url_path="home")
your_profile = st.Page("views/your_profile.py", title="Your Profile", url_path="your_profile")
additional_data = st.Page("views/additional_data.py", title="Additional Data", url_path="additional_data")
calculator = st.Page("views/caffeine_calculator.py", title="Caffeine Calculator", url_path="caffeine_calculator")
statistics = st.Page("views/statistic.py", title="History", url_path="statistic")
recommendations = st.Page("views/recommendations.py", title="Recommendations", url_path="recommendations")
alternatives = st.Page("views/alternatives.py", title="Alternatives", url_path="alternatives")
professional_help = st.Page("views/professional_help.py", title="Professional Help", url_path="professional_help")

pg = st.navigation([home1, your_profile, additional_data, calculator, statistics, recommendations, alternatives, professional_help])
pg.run()