import streamlit as st

# Titel
st.markdown(
    "<h1 style='color:#5C4033;'>Alternatives</h1>",
    unsafe_allow_html=True
)

st.write("")

# Styling
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    background-color: #CDECCF;
    color: black;
    border-radius: 10px;
    height: 60px;
    font-size: 16px;
    margin-bottom: 10px;
    border: none;
}

.info-box {
    border: 3px solid #CDECCF;
    border-radius: 12px;
    padding: 18px;
    margin-top: 20px;
    background-color: white;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# Texte
texts = {
    "Guarana": """
Guarana is a natural source of caffeine and a good caffeine alternative.  
The caffeine it contains is often released more slowly, so the effect may last longer and can feel gentler than some other caffeinated products.  
Guarana may help reduce tiredness and support concentration.  
A moderate daily amount is around 50–100 mg guarana extract or about 100–200 ml depending on the product.  
The total daily caffeine intake should generally stay below 400 mg per day.
""",
    "Green tea": """
Green tea is a mild caffeine alternative with a lower caffeine content than many other caffeinated products.  
Because it contains both caffeine and L-theanine, it can support concentration in a smoother way and may cause less nervousness.  
It also contains antioxidants that may support general health.  
A common recommendation is about 1–4 cups per day (100–500 ml).  
One cup usually contains around 30–50 mg caffeine.
""",
    "Ginger": """
Ginger is a caffeine-free alternative and is especially suitable for people who want to avoid caffeine completely.  
It may support digestion, has warming properties, and is often used when someone feels nausea or stomach discomfort.  
As a tea, it can be a good option for daily use.  
A common amount is about 1–3 cups per day (200–600 ml).
""",
    "Herbal tea": """
Herbal tea is an ideal caffeine-free alternative to caffeinated drinks.  
Depending on the type, it may have calming, digestive, or soothing effects.  
It is especially suitable in the evening or for people who are sensitive to caffeine.  
A common amount is about 1–5 cups per day (200–1000 ml) depending on the tea variety.
""",
    "Kokoa": """
Kokoa is a mild alternative to classic caffeine sources.  
It does not mainly act through caffeine, but contains compounds such as **theobromine**, which can have a gentle stimulating effect.  
Kokoa may also support mood and contains antioxidants.  
It is often enjoyed as a warm drink.  
A common recommendation is about 1–2 cups per day (200–400 ml), ideally with little sugar.
"""
}

# Auswahl speichern
if "selected_alternative" not in st.session_state:
    st.session_state.selected_alternative = None

# --- WITH CAFFEINE ---
st.markdown("<h3 style='color:black;'>With Caffeine</h3>", unsafe_allow_html=True)

if st.button("Guarana"):
    st.session_state.selected_alternative = "Guarana"

if st.button("Green tea"):
    st.session_state.selected_alternative = "Green tea"

st.write("")

# --- WITHOUT CAFFEINE ---
st.markdown("<h3 style='color:black;'>Without Caffeine</h3>", unsafe_allow_html=True)

if st.button("Ginger"):
    st.session_state.selected_alternative = "Ginger"

if st.button("Herbal tea"):
    st.session_state.selected_alternative = "Herbal tea"

if st.button("Kokoa"):
    st.session_state.selected_alternative = "Kokoa"

# Infobox unten anzeigen
if st.session_state.selected_alternative:
    selected = st.session_state.selected_alternative
    st.markdown(
        f"""
        <div class="info-box">
            <h4 style="color:#5C4033; margin-top:0;">{selected}</h4>
            <div>{texts[selected]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )