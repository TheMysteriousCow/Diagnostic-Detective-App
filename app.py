import pandas as pd
import streamlit as st
import pandas as pd

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
    df = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame()
    )

    if not df.empty:
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    st.session_state['data_df'] = df

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="diagnosticdetective"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---

home = st.Page("views/home.py", title="Home", icon="🏠")
calculator = st.Page("views/caffeine_calculator.py", title="Koffein Rechner", icon="☕")

pg = st.navigation([home, calculator])
pg.run()