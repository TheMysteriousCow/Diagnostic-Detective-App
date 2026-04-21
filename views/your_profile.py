import streamlit as st

st.markdown("""
<style>
/* Hintergrund weiß */
.stApp {
    background-color: white;
}

/* Allgemeine Schriftfarbe */
h1, h2, h3, h4, h5, h6, p, label {
    color: #5C4033 !important;
}

/* TITEL wie Hauptscreen */
.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# Titel im gleichen Stil wie Hauptseite
st.markdown(
    "<div class='main-title'>Your Profile</div>",
    unsafe_allow_html=True
)

st.write("")

name = st.text_input("Name")
first_name = st.text_input("First name")
gender = st.selectbox("Gender", ["Female", "Male", "Diverse"])
weight = st.text_input("Weight")
height = st.text_input("Height")