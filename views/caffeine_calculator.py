import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, date
from functions.caffeine_math import caffeine_remaining

st.markdown("""
<style>
.stApp {
    background-color: #FFFFFF;
}

.coffee-bean {
    position: fixed;
    top: -60px;
    width: 24px;
    height: 32px;
    background: 
        radial-gradient(circle at 35% 25%, #E8A855 0%, #C97C4C 15%, #8B4513 30%, #5C3317 60%, #2A1810 100%);
    border-radius: 50% 50% 55% 45% / 65% 60% 40% 45%;
    animation: fall linear forwards;
    pointer-events: none;
    box-shadow: 
        inset -4px -4px 8px rgba(0,0,0,0.7),
        inset 3px 2px 4px rgba(200,120,60,0.5),
        inset -2px -1px 3px rgba(0,0,0,0.9),
        inset 1px 1px 2px rgba(255,200,100,0.2),
        0px 6px 12px rgba(0,0,0,0.4);
    filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5)) brightness(0.95);
}

.coffee-bean::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(ellipse 50% 25% at 35% 20%, rgba(255,255,255,0.15), transparent 50%),
        radial-gradient(ellipse 30% 40% at 20% 60%, rgba(0,0,0,0.08), transparent),
        linear-gradient(135deg, rgba(200,100,50,0.1) 0%, transparent 50%, rgba(0,0,0,0.2) 100%);
    border-radius: inherit;
}

.coffee-bean::after {
    content: '';
    position: absolute;
    width: 3px;
    height: 65%;
    background: linear-gradient(90deg, rgba(0,0,0,0.5) 0%, rgba(60,30,15,0.3) 25%, rgba(0,0,0,0.3) 50%, rgba(60,30,15,0.3) 75%, rgba(0,0,0,0.5) 100%);
    top: 18%;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 2px;
    box-shadow: 1px 0 1px rgba(100,50,20,0.3);
}

@keyframes fall {
    to {
        transform: translateY(110vh) rotate(360deg);
        opacity: 0;
    }
}
</style>
""", unsafe_allow_html=True)

def coffee_rain():
    components.html("""
    <script>
    const beans = 120;
    const container = window.parent.document.body;

    for (let i = 0; i < beans; i++) {
        let bean = document.createElement("div");
        bean.className = "coffee-bean";

        // Random horizontal position
        bean.style.left = Math.random() * 100 + "vw";
        bean.style.animationDuration = (4 + Math.random()*4) + "s";

        container.appendChild(bean);

        setTimeout(() => {
            bean.remove();
        }, 3500);
    }
    </script>
    """, height=0)

st.title("☕ Koffeinabbau-Rechner")

with st.form("caffeine_form"):

    drink = st.selectbox(
        "Getränk",
        ["Kaffee","Espresso","Energy Drink","Red Bull","NOCCO","Mate","Matcha","Schwarzer Tee","Eigener Wert"]
    )

    default_values = {
        "Kaffee":95,
        "Espresso":60,
        "Energy Drink":80,
        "Red Bull":80,
        "NOCCO":180,
        "Mate":80,
        "Matcha":70,
        "Schwarzer Tee":45,
        "Eigener Wert":0
    }

    col1, col2 = st.columns(2)
    
    with col1:
        caffeine_per_ml = st.number_input(
            "Koffein pro ml (mg/ml)",
            min_value=0.0,
            max_value=50.0,
            value=float(default_values[drink] / 250 if drink != "Eigener Wert" else 0.0),
            step=0.1
        )
    
    with col2:
        volume_ml = st.number_input(
            "Getränkemenge (ml)",
            min_value=1.0,
            max_value=1000.0,
            value=250.0,
            step=10.0
        )
    
    dose_mg = caffeine_per_ml * volume_ml

    half_life = st.slider(
        "Halbwertszeit (Stunden)",
        min_value=2.0,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

    intake_time = st.time_input(
        "Uhrzeit der Einnahme",
        value=datetime.now().time().replace(second=0, microsecond=0)
    )

    horizon = st.slider(
        "Berechnungszeitraum (Stunden)",
        min_value=6,
        max_value=48,
        value=24
    )

    submit = st.form_submit_button("Ausrechnen")

if submit:

    coffee_rain()

    now = datetime.now()
    taken_at = datetime.combine(date.today(), intake_time)

    hours_since = (now - taken_at).total_seconds() / 3600

    current = caffeine_remaining(dose_mg, hours_since, half_life)

    caffeine_zero_time = None
    for h in range(1, horizon + 1):
        if caffeine_remaining(dose_mg, h, half_life) < 0.5:
            caffeine_zero_time = h
            break

    st.metric("Koffein aktuell im Körper (mg)", f"{current:.1f}")

    if caffeine_zero_time:
        st.success(f"✅ Koffein ist nach ca. {caffeine_zero_time} Stunde(n) aus dem Körper")
    
    data = []

    for h in range(horizon + 1):

        remaining = caffeine_remaining(dose_mg, h, half_life)

        data.append({
            "Stunden": h,
            "Koffein (mg)": remaining
        })

    df = pd.DataFrame(data).set_index("Stunden")

    st.line_chart(df)