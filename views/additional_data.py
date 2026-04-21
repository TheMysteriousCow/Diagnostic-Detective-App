import streamlit as st

# Globales Styling + Titelstil
st.markdown("""
<style>
/* Schrift allgemein */
h1, h2, h3, h4, h5, h6, p, label {
    color: #5C4033 !important;
}

/* Titel wie im Hauptscreen */
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

# Titel im gleichen Stil
st.markdown(
    "<div class='main-title'>Additional Data</div>",
    unsafe_allow_html=True
)

st.write("")

# Previous illness
st.markdown("<h3>Previous illness</h3>", unsafe_allow_html=True)
illness_list = st.text_area("Enter previous illnesses (one per line)")

# Medication
st.markdown("<h3>Medication</h3>", unsafe_allow_html=True)
medication_list = st.text_area("Enter medications (one per line)")