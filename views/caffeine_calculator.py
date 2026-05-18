import os
import streamlit as st

from utils.profile_utils import load_profile
from functions.logo import set_logo

from functions.caffeine_calculator_math import (
    safe_float,
    initialize_caffeine_session,
    restore_active_countdown_to_session,
)

from functions.caffeine_calculator_data import (
    load_history,
    load_current,
    get_page_css,
    render_header,
    render_drink_selector,
    render_caffeine_timeline,
    render_current_entries,
    render_personal_impact,
)


st.set_page_config(page_title="Caffeine Calculator", layout="wide")

username = st.session_state.get("username")

if username is None:
    st.error("No user logged in.")
    st.stop()

profile = load_profile(username)
profile_weight = safe_float(profile.get("weight", ""))
profile_height = safe_float(profile.get("height", ""))

image_path = os.path.join(os.getcwd(), "images", "logo.png")

set_logo(
    image_path,
    top=-40,
    right=-20,
    width=140
)

st.markdown(get_page_css(), unsafe_allow_html=True)

initialize_caffeine_session(load_history, load_current)
restore_active_countdown_to_session(load_current)

render_header()
render_drink_selector()
render_caffeine_timeline()
render_current_entries()
render_personal_impact(profile_weight, profile_height)