import streamlit as st
import base64
import os


# =========================
# Logo Funktion
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
        top: 7px;
        right: -23px;
        z-index: 100;
    }}

    .logo-img {{
        width: 170px;
        height: auto;
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{encoded}" class="logo-img">
    </div>
    """

    st.markdown(css, unsafe_allow_html=True)


# =========================
# Logo anzeigen
# =========================
image_path = os.path.join(os.getcwd(), "images", "logo.png")
set_logo_top_right(image_path)


# =========================
# Styling
# =========================
st.markdown("""
<style>
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
    "<div class='main-title'>Additional Data</div>",
    unsafe_allow_html=True
)

st.write("")


# =========================
# Inhalte
# =========================
st.markdown("<h3>Previous illness</h3>", unsafe_allow_html=True)
illness_list = st.text_area("Enter previous illnesses (one per line)")

st.markdown("<h3>Medication</h3>", unsafe_allow_html=True)
medication_list = st.text_area("Enter medications (one per line)")