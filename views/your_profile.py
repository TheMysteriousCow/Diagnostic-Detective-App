import streamlit as st
import base64
import os


# =========================
# Logo Funktion (gleich wie Login)
# =========================
def set_logo_top_right(image_file: str):
    if not os.path.exists(image_file):
        st.warning(f"Bild konnte nicht geladen werden. Pfad: {image_file}")
        return

    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    .logo-container {{
        position: absolute;
        top: -45px;   /* gleiche Position wie Login */
        right: 0px;
        z-index: 100;
    }}
    .logo-img {{
        width: 140px;   /* 👈 deine gewünschte Größe */
        height: auto;
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{encoded}" class="logo-img">
    </div>
    """

    st.markdown(css, unsafe_allow_html=True)


# =========================
# Logo einfügen (GANZ OBEN!)
# =========================
image_path = os.path.join(os.getcwd(), "images", "logo.png")
set_logo_top_right(image_path)


# =========================
# Styling
# =========================
st.markdown("""
<style>
.stApp {
    background-color: white;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: #5C4033 !important;
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
</style>
""", unsafe_allow_html=True)


# =========================
# Titel
# =========================
st.markdown(
    "<div class='main-title'>Your Profile</div>",
    unsafe_allow_html=True
)

st.write("")


# =========================
# Eingabefelder
# =========================
name = st.text_input("Name")
first_name = st.text_input("First name")
gender = st.selectbox("Gender", ["Female", "Male", "Diverse"])
weight = st.text_input("Weight")
height = st.text_input("Height")