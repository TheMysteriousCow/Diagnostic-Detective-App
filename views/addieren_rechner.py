import streamlit as st
from functions.addieren import add

st.title("Unterseite A")

st.write("Hier ist mein Rechner")

with st.form("addition_form"):
    nummer_1 = st.number_input("Zahl 1")
    nummer_2 = st.number_input("Zahl 2")

    # submit button for the form
    submit_button = st.form_submit_button("Berechnen")

    # calculate only after submission
    if submit_button:
        resultat = add(nummer_1, nummer_2)
        st.write(f"Ergebnis: {resultat}")

