import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# -----------------------------
# GLOBAL STYLE (MATCH ADDITIONAL DATA)
# -----------------------------
st.markdown("""
<style>

/* Gesamt Schrift */
html, body, [class*="css"] {
    font-family: 'Georgia', 'Times New Roman', serif;
    color: #5a3e36;
}

/* Titel */
h1 {
    font-family: 'Georgia', serif;
    color: #5a3e36 !important;
    font-weight: 700;
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
# PAGE CONFIG / TITLE
# -----------------------------
st.title("Recommendations")
st.caption("Understand your caffeine state and get direct help.")


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
    x = np.linspace(0, total_hours, 600)

    # Sanfter Anstieg bis ca. Stunde 5
    rise = smoothstep(x, 0.0, 5.0)

    # Sanfter, kontinuierlicher Abfall nach dem Peak
    decay = np.exp(-0.28 * np.clip(x - 5.0, 0, None))

    y = rise * decay

    # auf 1 normieren
    y = y / np.max(y)

    # leichte Skalierung je nach Menge, ohne die Kurvenform kaputt zu machen
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
# MAIN PAGE
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