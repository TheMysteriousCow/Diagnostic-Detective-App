import streamlit as st

st.set_page_config(page_title="Caffeine Calculator", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    font-style: italic;
    color: #5C4033;
    margin-bottom: 2.5rem;
    font-family: 'Georgia', 'Times New Roman', serif;
}

.menu-wrap {
    display: flex;
    flex-direction: column;
    gap: 26px;
    margin-top: 1rem;
}

.menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 120px;
    text-decoration: none !important;
    font-size: 1.5rem;
    font-weight: 500;
    font-family: Arial, sans-serif;
    border: none;
    color: #6b4a3b !important;
    box-sizing: border-box;
    transition: transform 0.12s ease, filter 0.12s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    border-radius: 12px;
}

.menu-btn:hover {
    filter: brightness(0.97);
    transform: scale(1.01);
}

/* Farben */
.profile { background-color: #FFF4B8; }
.data { background-color: #FFD8B1; }
.calculator { background-color: #F7C6C7; }
.statistic { background-color: #E7A8C9; }
.recommendations { background-color: #F8D6E6; }
.alternatives { background-color: #CFE8FF; }
.help {
    background-color: #6FA3CC;
    color: #6b4a3b !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Caffeine Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Track it. Understand it. Control it.</div>", unsafe_allow_html=True)

left, center, right = st.columns([1.2, 1.6, 1.2])

with center:
    st.markdown("""
    <div class="menu-wrap">
        <a class="menu-btn profile" href="/your_profile" target="_self">Your Profile</a>
        <a class="menu-btn data" href="/additional_data" target="_self">Additional Data</a>
        <a class="menu-btn calculator" href="/caffeine_calculator" target="_self">Caffeine Calculator</a>
        <a class="menu-btn statistic" href="/statistic" target="_self">History</a>
        <a class="menu-btn recommendations" href="/recommendations" target="_self">Recommendations</a>
        <a class="menu-btn alternatives" href="/alternatives" target="_self">Alternatives</a>
        <a class="menu-btn help" href="/professional_help" target="_self">Professional Help</a>
    </div>
    """, unsafe_allow_html=True)