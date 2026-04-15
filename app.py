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

home = st.Page("views/home.py", title="Home", icon="🏠")
your_profile = st.Page("views/your_profile.py", title="Your Profile", icon="☕")
additional_data = st.Page("views/additional_data.py", title="Additional Data", icon="☕")
home1 = st.Page("views/home1.py", title="Home", icon="☕")
calculator = st.Page("views/caffeine_calculator.py", title="Koffein Rechner", icon="☕")
statistics = st.Page("views/statistic.py", title="Statistik", icon="☕")
recommendations = st.Page("views/recommendations.py", title="Recommendations", icon="☕")
alternatives = st.Page("views/alternatives.py", title="Alternatives", icon="☕")

pg = st.navigation([home, your_profile, additional_data, home1, calculator, statistics, recommendations, alternatives])
pg.run()