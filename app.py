import streamlit as st
import pandas as pd

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Data manager initialisieren
data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="diagnosticdetective"
)

# Für andere Seiten verfügbar machen
st.session_state["data_manager"] = data_manager

# Login
login_manager = LoginManager(data_manager)
login_manager.login_register()

# User-Daten laden
if 'data_df' not in st.session_state:
    df = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame()
    )

    # Falls Datei existiert, aber noch alte Struktur hat:
    if not df.empty:
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    st.session_state['data_df'] = df

home = st.Page("views/home.py", title="Home", icon="🏠")
calculator = st.Page("views/caffeine_calculator.py", title="Koffein Rechner", icon="☕")

pg = st.navigation([home, calculator])
pg.run()