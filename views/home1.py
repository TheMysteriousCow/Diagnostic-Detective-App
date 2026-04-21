import streamlit as st

st.set_page_config(page_title="Caffeine Calculator", layout="wide")

# -------------------------------------------------
# CSS (Design + Layout)
# -------------------------------------------------
st.markdown("""
<style>

/* Abstand */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* TITEL */
.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

/* SLOGAN */
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    font-style: italic;
    color: #5C4033;
    margin-bottom: 2.5rem;
    font-family: 'Georgia', 'Times New Roman', serif;
}

/* BUTTON STYLE */
div[data-testid="stButton"] > button {
    width: 100%;
    height: 80px;
    font-size: 1.5rem;
    font-weight: 600;
    border-radius: 0px;
    border: 4px solid #5C4033;
    color: #5C4033;
    box-shadow: none;
    transition: 0.15s;
}

/* Hover */
div[data-testid="stButton"] > button:hover {
    filter: brightness(0.97);
}

/* Fokus entfernen */
div[data-testid="stButton"] > button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Farben exakt pro Button (mittlere Spalte!) */
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(1) > button {
    background-color: #f3cfe0 !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(2) > button {
    background-color: #f0c5d7 !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(3) > button {
    background-color: #f7f3bf !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(4) > button {
    background-color: #cfe7ff !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(5) > button {
    background-color: #d7f5c9 !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(6) > button {
    background-color: #c9f2c8 !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(7) > button {
    background-color: #f7b5a8 !important;
}
section.main div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(8) > button {
    background-color: #4db3ff !important;
    color: #5C4033 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITEL + SLOGAN
# -------------------------------------------------
st.markdown("<div class='main-title'>Caffeine Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>track it. understand it. control it</div>", unsafe_allow_html=True)

# -------------------------------------------------
# MITTIGE BUTTONS
# -------------------------------------------------
left, center, right = st.columns([1.2, 1.6, 1.2])

with center:
    if st.button("Home", use_container_width=True):
        st.switch_page("views/home.py")

    if st.button("Calculator", use_container_width=True):
        st.switch_page("views/caffeine_calculator.py")

    if st.button("Statistic", use_container_width=True):
        st.switch_page("views/statistic.py")

    if st.button("Recommendations", use_container_width=True):
        st.switch_page("views/recommendations.py")

    if st.button("Alternatives", use_container_width=True):
        st.switch_page("views/alternatives.py")

    if st.button("Professional Help", use_container_width=True):
        st.switch_page("views/professional_help.py")

    if st.button("Additional Data", use_container_width=True):
        st.switch_page("views/additional_data.py")

    if st.button("Your Profile", use_container_width=True):
        st.switch_page("views/your_profile.py")