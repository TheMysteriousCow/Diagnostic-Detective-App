import os
import streamlit as st
from functions.logo import set_logo
from functions.recommendations_status import load_history_data, show_caffeine_status
from functions.recommendations_choosehowyoufeel import (
    show_selected_detail,
    show_choose_how_you_feel
)


st.set_page_config(page_title="Recommendations", layout="wide")


image_path = os.path.join(os.getcwd(), "images", "logo.png")

set_logo(
    image_path,
    top=-40,
    right=-20,
    width=140
)


st.markdown("""
<style>
.stApp {
    background-color: white;
    color: #5C4033 !important;
}

html, body, p, div, span, label,
h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, .stCaption,
[data-testid="stMarkdownContainer"],
[data-testid="stText"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stWidgetLabel"] {
    color: #5C4033 !important;
}

.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033 !important;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    font-family: Arial, sans-serif;
    color: #5C4033 !important;
    margin-bottom: 2rem;
}

h2, h3 {
    font-family: 'Georgia', serif;
    color: #5C4033 !important;
}

div.stButton > button {
    width: 100%;
    height: 50px;
    background-color: #CDECCF;
    color: #5C4033 !important;
    border: none;
    border-radius: 16px;
    font-size: 1rem;
    font-family: Arial, sans-serif;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #BEE6C2;
    color: #5C4033 !important;
}

.streamlit-expanderHeader {
    font-family: 'Georgia', serif;
    color: #5C4033 !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='main-title'>Recommendations</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand your caffeine state and get direct help.</div>", unsafe_allow_html=True)


if "recommendation_detail" not in st.session_state:
    st.session_state["recommendation_detail"] = None

if "data_df" not in st.session_state:
    st.session_state["data_df"] = load_history_data()


show_selected_detail()
show_caffeine_status()
show_choose_how_you_feel()