import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -----------------------------
# GLOBAL STYLE
# -----------------------------
st.markdown("""
<style>

/* Gesamt Schrift */
html, body, [class*="css"] {
    font-family: 'Georgia', 'Times New Roman', serif;
    color: #5a3e36;
}

/* Titel wie auf allen Seiten */
.main-title {
    text-align: center;
    font-size: 3.4rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-weight: 600;
    color: #5C4033;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}

/* Untertitel (normale Schrift) */
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    font-family: Arial, sans-serif;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* Untertitel */
h2, h3 {
    font-family: 'Georgia', serif;
    color: #5a3e36 !important;
}

/* Texte */
p, span, label {
    color: #5a3e36 !important;
}

/* Metrics */
[data-testid="stMetricLabel"] {
    color: #5a3e36 !important;
    font-family: 'Georgia', serif;
}

[data-testid="stMetricValue"] {
    color: #5a3e36 !important;
    font-family: 'Georgia', serif;
}

/* Buttons */
.stButton > button {
    font-family: 'Georgia', serif;
    color: #5a3e36;
    border-radius: 10px;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Georgia', serif;
    color: #5a3e36 !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<div class='main-title'>Recommendations</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand your caffeine state and get direct help.</div>", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

if "recommendation_detail" not in st.session_state:
    st.session_state["recommendation_detail"] = None

data_df = st.session_state["data_df"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
HALF_LIFE = 5.0

def caffeine_remaining(initial_mg: float, hours_passed: float, half_life: float = 5.0) -> float:
    if initial_mg <= 0:
        return 0.0
    if hours_passed < 0:
        hours_passed = 0.0
    return initial_mg * (0.5 ** (hours_passed / half_life))

def get_latest_entry(df: pd.DataFrame):
    if df.empty:
        return None

    df_copy = df.copy()

    if "timestamp" in df_copy.columns:
        df_copy["timestamp"] = pd.to_datetime(df_copy["timestamp"], errors="coerce")
        df_copy = df_copy.dropna(subset=["timestamp"]).sort_values("timestamp")

    if df_copy.empty:
        return None

    return df_copy.iloc[-1]

def get_hours_since_latest_entry(entry) -> float:
    if entry is None or "timestamp" not in entry:
        return 0.0

    ts = pd.to_datetime(entry["timestamp"], errors="coerce")
    if pd.isna(ts):
        return 0.0

    now = pd.Timestamp.now()
    hours_passed = (now - ts).total_seconds() / 3600
    return max(0.0, hours_passed)

def get_phase_info(hours_passed: float):
    if hours_passed < 2:
        return "Start", "Caffeine is just entering your body."
    elif hours_passed < 4:
        return "Increase", "The effect is building up."
    elif hours_passed < 6:
        return "Peak", "The caffeine effect is strongest now."
    elif hours_passed < 8:
        return "Crash", "The effect is going down again."
    else:
        return "Recovery", "Your body is slowly calming down."

def smoothstep(x, edge0, edge1):
    t = np.clip((x - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)

def build_curve(initial_mg: float, total_hours: int = 10):
    x = np.linspace(0, total_hours, 800)

    rise = smoothstep(x, 0.0, 5.0)
    t_after_peak = np.clip(x - 5.0, 0, None)
    decay = np.exp(-0.22 * (t_after_peak ** 1.6))

    y = rise * decay
    y = y / np.max(y)

    scale = max(0.85, min(initial_mg / 100, 1.15))
    y = y * scale

    return x, y

def add_vertical_gradient(ax, x0, x1, y0, y1, color_rgb, alpha_top=0.40, alpha_bottom=0.18, zorder=0):
    n = 256
    gradient = np.ones((n, 2, 4))
    gradient[..., 0] = color_rgb[0]
    gradient[..., 1] = color_rgb[1]
    gradient[..., 2] = color_rgb[2]
    gradient[..., 3] = np.linspace(alpha_top, alpha_bottom, n).reshape(n, 1)

    ax.imshow(
        gradient,
        aspect="auto",
        extent=[x0, x1, y0, y1],
        origin="lower",
        zorder=zorder
    )

def draw_phase_bar(ax):
    bar_y = -0.02
    bar_height = 0.12

    phase_specs = [
        ("Start", 0, 2, "#b7df72"),
        ("Increase", 2, 4, "#76bb2d"),
        ("Peak", 4, 6, "#ff4338"),
        ("Crash", 6, 8, "#ff9d35"),
        ("Recovery", 8, 10, "#7aa8cf"),
    ]

    for label, x0, x1, color in phase_specs:
        rect = patches.Rectangle(
            (x0, bar_y),
            x1 - x0,
            bar_height,
            facecolor=color,
            edgecolor="none",
            alpha=0.95,
            zorder=3
        )
        ax.add_patch(rect)
        ax.text(
            (x0 + x1) / 2,
            bar_y + bar_height / 2,
            label,
            ha="center",
            va="center",
            fontsize=13,
            color="white" if label != "Start" else "#1f1f1f",
            zorder=4
        )

def plot_colored_segments(ax, x, y):
    phase_segments = [
        (0, 2, "#7da61b"),
        (2, 4, "#76bb2d"),
        (4, 6, "#ff4338"),
        (6, 8, "#ff9d35"),
        (8, 10, "#2f6fb0"),
    ]

    for x0, x1, color in phase_segments:
        mask = (x >= x0) & (x <= x1)
        ax.plot(x[mask], y[mask], color=color, linewidth=3, zorder=5)

# -----------------------------
# DETAIL PAGE
# -----------------------------
def show_detail_page(title: str, intro: str, tips: list[str], warning: str):
    st.subheader(title)
    st.write(intro)

    st.markdown("### What can help?")
    for tip in tips:
        st.write(f"• {tip}")

    st.markdown("### Important")
    st.warning(warning)

    if st.button("Back"):
        st.session_state["recommendation_detail"] = None
        st.rerun()

# -----------------------------
# HELP SECTION
# -----------------------------
def show_phase_help():
    st.markdown("### Help: What do the phases mean?")

    with st.expander("Start"):
        st.write("Caffeine has just entered your body. You usually do not feel the full effect yet.")

    with st.expander("Increase"):
        st.write("The caffeine effect is getting stronger. You may start to feel more awake, focused or active.")

    with st.expander("Peak"):
        st.write("This is the strongest phase. The caffeine effect is highest now.")

    with st.expander("Crash"):
        st.write("The caffeine effect starts to go down again. Some people feel more tired, unfocused or low in energy here.")

    with st.expander("Recovery"):
        st.write("Your body is slowly calming down again. The caffeine level is lower and the effect becomes weaker.")

# -----------------------------
# DETAIL ROUTING
# -----------------------------
selected_detail = st.session_state["recommendation_detail"]

if selected_detail == "Peak":
    show_detail_page(
        title="Peak",
        intro="Your caffeine effect is currently high. This is the phase in which alertness and stimulation are strongest.",
        tips=[
            "Avoid additional caffeine right now.",
            "Drink water to stay hydrated.",
            "Use this phase for focused work, but do not overdo it.",
            "If you feel shaky, take a short break and eat something light."
        ],
        warning="Too much caffeine during the peak phase can increase nervousness, inner restlessness and heartbeat."
    )
    st.stop()

elif selected_detail == "I can't fall asleep":
    show_detail_page(
        title="I can't fall asleep",
        intro="There may still be too much caffeine in your body, especially if you consumed it late in the day.",
        tips=[
            "Do not take more caffeine today.",
            "Avoid screens and bright light before sleep.",
            "Drink water, but not too much right before bed.",
            "Try a calm environment and slow breathing."
        ],
        warning="If sleep problems happen often, reduce caffeine in the afternoon and evening."
    )
    st.stop()

elif selected_detail == "I feel tired":
    show_detail_page(
        title="I feel tired",
        intro="Your caffeine effect may already be dropping. This can happen after the stimulating phase wears off.",
        tips=[
            "Drink water first.",
            "Eat a balanced snack.",
            "Get fresh air or move for a few minutes.",
            "Avoid automatically taking more caffeine immediately."
        ],
        warning="Repeated caffeine use against tiredness can lead to a cycle of short-term stimulation and later tiredness."
    )
    st.stop()

elif selected_detail == "I feel anxious":
    show_detail_page(
        title="I feel anxious",
        intro="High caffeine levels can increase nervousness, restlessness or tension.",
        tips=[
            "Stop caffeine for the rest of the day.",
            "Drink water slowly.",
            "Sit down and breathe slowly and deeply.",
            "Reduce other stimulants if possible."
        ],
        warning="If symptoms are strong or unusual, professional medical advice may be necessary."
    )
    st.stop()

elif selected_detail == "I can't concentrate":
    show_detail_page(
        title="I can't concentrate",
        intro="Too little or too much caffeine can both affect concentration.",
        tips=[
            "Check whether you are in a crash phase or overstimulated.",
            "Drink water and take a short movement break.",
            "Work in short blocks instead of forcing long focus periods.",
            "Avoid taking more caffeine too quickly."
        ],
        warning="Poor concentration is not always caused by caffeine. Sleep, stress and food intake also matter."
    )
    st.stop()

elif selected_detail == "Recovery":
    show_detail_page(
        title="Recovery",
        intro="Your body is slowly returning to a calmer state. The caffeine effect is lower now.",
        tips=[
            "Drink water and listen to your natural energy level.",
            "Fresh air, food or rest may help more than another coffee.",
            "Use this phase to return to a more balanced rhythm.",
            "Avoid taking caffeine automatically just because the effect is fading."
        ],
        warning="If you often rely on caffeine again during recovery, it can become a repeating cycle."
    )
    st.stop()

# -----------------------------
# CHART
# -----------------------------
def draw_recommendation_chart(initial_mg: float, hours_passed: float):
    x, y = build_curve(initial_mg)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    y_max = max(1.08, float(np.max(y) + 0.08))

    add_vertical_gradient(ax, 0, 2, 0, y_max, (183/255, 223/255, 114/255))
    add_vertical_gradient(ax, 2, 4, 0, y_max, (190/255, 214/255, 84/255))
    add_vertical_gradient(ax, 4, 6, 0, y_max, (1.0, 84/255, 78/255))
    add_vertical_gradient(ax, 6, 8, 0, y_max, (243/255, 176/255, 104/255))
    add_vertical_gradient(ax, 8, 10, 0, y_max, (163/255, 194/255, 223/255))

    for border_x in [2, 4, 6, 8]:
        ax.axvline(border_x, color=(0, 0, 0, 0.08), linewidth=1)

    plot_colored_segments(ax, x, y)

    current_x = min(hours_passed, 10)
    current_y = np.interp(current_x, x, y)

    ax.scatter(current_x, current_y, s=110, color="#0d4f8b", zorder=6)

    text_x = current_x + 0.12 if current_x < 8.8 else current_x - 1.25
    text_ha = "left" if current_x < 8.8 else "right"

    ax.text(
        text_x,
        current_y + 0.08,
        "You are here",
        fontsize=16,
        color="#1f1f1f",
        ha=text_ha,
        va="bottom",
        zorder=7
    )

    draw_phase_bar(ax)

    ax.set_title("Caffeine state over time", fontsize=20, pad=8)
    ax.set_xlabel("Hours", fontsize=16)
    ax.set_ylabel("Effect", fontsize=16)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, y_max)
    ax.set_xticks(np.arange(0, 11, 2))
    ax.tick_params(axis="both", labelsize=12)
    ax.grid(True, alpha=0.12)

    st.pyplot(fig, clear_figure=True)

# -----------------------------
# MAIN
# -----------------------------
latest_entry = get_latest_entry(data_df)

if latest_entry is None:
    st.info("No caffeine data available yet. Please use the Caffeine Calculator first.")
    st.stop()

initial_mg = float(latest_entry.get("Koffeinmenge zu Beginn (mg)", 0))
hours_passed = get_hours_since_latest_entry(latest_entry)
current_mg = caffeine_remaining(initial_mg, hours_passed, HALF_LIFE)

phase_name, phase_text = get_phase_info(hours_passed)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Initial caffeine", f"{initial_mg:.1f} mg")
with col2:
    st.metric("Estimated current caffeine", f"{current_mg:.1f} mg")
with col3:
    st.metric("Current phase", phase_name)

draw_recommendation_chart(initial_mg, hours_passed)

st.success(f"Current interpretation: **{phase_name}** — {phase_text}")

st.markdown("### Choose how you feel")

col_a, col_b = st.columns(2)

with col_a:
    if st.button("Peak", use_container_width=True):
        st.session_state["recommendation_detail"] = "Peak"
        st.rerun()

    if st.button("I feel tired", use_container_width=True):
        st.session_state["recommendation_detail"] = "I feel tired"
        st.rerun()

    if st.button("I feel anxious", use_container_width=True):
        st.session_state["recommendation_detail"] = "I feel anxious"
        st.rerun()

with col_b:
    if st.button("I can't fall asleep", use_container_width=True):
        st.session_state["recommendation_detail"] = "I can't fall asleep"
        st.rerun()

    if st.button("I can't concentrate", use_container_width=True):
        st.session_state["recommendation_detail"] = "I can't concentrate"
        st.rerun()

    if st.button("Recovery", use_container_width=True):
        st.session_state["recommendation_detail"] = "Recovery"
        st.rerun()

show_phase_help()