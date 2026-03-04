import streamlit as st

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:")
pg_second = st.Page("views/addieren_rechner.py", title="Unterseite A")

pg = st.navigation([pg_home, pg_second])
pg.run()

