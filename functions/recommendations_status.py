import time
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.data_manager import DataManager
from functions.caffeine_calculator_data import empty_current_data


PEAK_HOURS = 0.75
CRASH_HOURS = 4
RECOVERY_HOURS = 8
TOTAL_HOURS = 10
HALF_LIFE = 5.0


def get_data_files():
    #username = st.session_state.get("username", "default_user")#
    return f"data.csv", f"current_caffeine.json"


def get_data_manager():
    return DataManager(
        fs_protocol="webdav",
        fs_root_folder="caffeine_calculator_app"
    )


def load_current_data():
    _, current_file = get_data_files()
    data_manager = get_data_manager()

    data = data_manager.load_user_data(
        current_file,
        initial_value=empty_current_data()
    )

    if not isinstance(data, dict):
        return empty_current_data()

    data.setdefault("entries", [])
    data.setdefault("countdown_end_time", None)
    data.setdefault("countdown_total_seconds", 0)
    data.setdefault("last_drink", None)

    return data


def load_history_data():
    data_file, _ = get_data_files()
    data_manager = get_data_manager()

    df = data_manager.load_user_data(
        data_file,
        initial_value=pd.DataFrame(columns=[
            "timestamp",
            "Drink",
            "Caffeine (mg)",
            "Volume (ml)"
        ])
    )

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

    return df


def caffeine_remaining(initial_mg: float, hours_passed: float, half_life: float = 5.0) -> float:
    if initial_mg <= 0:
        return 0.0

    hours_passed = max(hours_passed, 0.0)
    return initial_mg * (0.5 ** (hours_passed / half_life))


def get_phase_info(hours_passed: float):
    if hours_passed < PEAK_HOURS:
        return "Increase", "The caffeine effect is building up and has not reached the peak yet."
    elif hours_passed < CRASH_HOURS:
        return "Peak", "The caffeine effect is strong now."
    elif hours_passed < RECOVERY_HOURS:
        return "Crash", "The caffeine effect is going down again."
    else:
        return "Recovery", "Your body is slowly calming down again."


def get_latest_entry(df: pd.DataFrame):
    if df.empty:
        return None

    df_copy = df.copy()
    df_copy["timestamp"] = pd.to_datetime(df_copy["timestamp"], errors="coerce")
    df_copy = df_copy.dropna(subset=["timestamp"]).sort_values("timestamp")

    if df_copy.empty:
        return None

    return df_copy.iloc[-1]


def get_hours_since_timestamp(timestamp) -> float:
    ts = pd.to_datetime(timestamp, errors="coerce")

    if pd.isna(ts):
        return 0.0

    return max(0.0, (pd.Timestamp.now() - ts).total_seconds() / 3600)


def get_initial_caffeine(entry) -> float:
    try:
        return float(entry.get("Caffeine (mg)", 0))
    except:
        return 0.0


def build_curve(total_hours: int = 10):
    x = np.linspace(0, total_hours, 1000)
    y = np.zeros_like(x)

    for i, hour in enumerate(x):
        if hour <= PEAK_HOURS:
            y[i] = hour / PEAK_HOURS
        else:
            y[i] = np.exp(-0.32 * (hour - PEAK_HOURS))

    return x, y


def add_vertical_gradient(ax, x0, x1, y0, y1, color_rgb, alpha_top=0.35, alpha_bottom=0.15, zorder=0):
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
    bar_y = -0.10
    bar_height = 0.08

    phase_specs = [
        ("Increase", 0, PEAK_HOURS, "#76bb2d"),
        ("Peak", PEAK_HOURS, CRASH_HOURS, "#ff4338"),
        ("Crash", CRASH_HOURS, RECOVERY_HOURS, "#ff9d35"),
        ("Recovery", RECOVERY_HOURS, TOTAL_HOURS, "#7aa8cf"),
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
            fontsize=11,
            color="white",
            zorder=4
        )


def plot_colored_segments(ax, x, y):
    phase_segments = [
        (0, PEAK_HOURS, "#76bb2d"),
        (PEAK_HOURS, CRASH_HOURS, "#ff4338"),
        (CRASH_HOURS, RECOVERY_HOURS, "#ff9d35"),
        (RECOVERY_HOURS, TOTAL_HOURS, "#2f6fb0"),
    ]

    for x0, x1, color in phase_segments:
        mask = (x >= x0) & (x <= x1)
        ax.plot(x[mask], y[mask], color=color, linewidth=3, zorder=5)


def draw_recommendation_chart(hours_passed: float):
    x, y = build_curve(TOTAL_HOURS)

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    y_max = 1.1

    add_vertical_gradient(ax, 0, PEAK_HOURS, 0, y_max, (118/255, 187/255, 45/255))
    add_vertical_gradient(ax, PEAK_HOURS, CRASH_HOURS, 0, y_max, (1.0, 67/255, 56/255))
    add_vertical_gradient(ax, CRASH_HOURS, RECOVERY_HOURS, 0, y_max, (1.0, 157/255, 53/255))
    add_vertical_gradient(ax, RECOVERY_HOURS, TOTAL_HOURS, 0, y_max, (122/255, 168/255, 207/255))

    for border_x in [PEAK_HOURS, CRASH_HOURS, RECOVERY_HOURS]:
        ax.axvline(border_x, color=(0, 0, 0, 0.15), linewidth=1)

    plot_colored_segments(ax, x, y)

    current_x = min(max(hours_passed, 0), TOTAL_HOURS)
    current_y = np.interp(current_x, x, y)

    ax.scatter(current_x, current_y, s=120, color="#0d4f8b", zorder=6)

    if current_x < 8.7:
        text_x = current_x + 0.15
        text_ha = "left"
    else:
        text_x = current_x - 0.25
        text_ha = "right"

    ax.text(
        text_x,
        min(current_y + 0.06, 1.05),
        "You are here",
        fontsize=14,
        color="#1f1f1f",
        ha=text_ha,
        va="bottom",
        zorder=7
    )

    draw_phase_bar(ax)

    ax.set_title("Caffeine state over time", fontsize=20, pad=12, color="#5C4033")
    ax.set_xlabel("Hours after caffeine intake", fontsize=14, color="#5C4033")
    ax.set_ylabel("Effect strength", fontsize=14, color="#5C4033")

    ax.set_xlim(0, TOTAL_HOURS)
    ax.set_ylim(-0.12, y_max)
    ax.set_xticks([0, PEAK_HOURS, 2, CRASH_HOURS, 6, RECOVERY_HOURS, 10])
    ax.set_xticklabels(["0", "0.75", "2", "4", "6", "8", "10"])

    ax.tick_params(axis="both", labelsize=11, colors="#5C4033")
    ax.grid(True, alpha=0.12)

    st.pyplot(fig, clear_figure=True)


def show_phase_help():
    st.markdown("### Help: What do the phases mean?")

    with st.expander("Increase"):
        st.write("Caffeine is entering your body. The effect is rising and usually reaches its peak after about 45 minutes.")

    with st.expander("Peak"):
        st.write("This is the strongest phase. In this app, the peak starts after about 45 minutes and lasts until around 4 hours.")

    with st.expander("Crash"):
        st.write("The caffeine effect is going down. Some people feel tired, unfocused or low in energy here.")

    with st.expander("Recovery"):
        st.write("Your body is slowly calming down again. The caffeine effect is weaker now.")


def get_caffeine_status():
    current_data = load_current_data()
    current_entries = current_data.get("entries", [])
    end_time = current_data.get("countdown_end_time")
    now_unix = int(time.time())

    has_active_countdown = bool(current_entries) and end_time and end_time > now_unix

    if has_active_countdown:
        current_df = pd.DataFrame(current_entries)

        current_df["timestamp"] = pd.to_datetime(
            current_df["timestamp"],
            errors="coerce"
        )

        current_df = current_df.dropna(subset=["timestamp"])

        if current_df.empty:
            st.info("No valid active caffeine data found. Please use the Caffeine Calculator first.")
            st.stop()

        current_df = current_df.sort_values("timestamp")

        first_timestamp = current_df.iloc[0]["timestamp"]
        initial_mg = current_df["Caffeine (mg)"].sum()
        hours_passed = get_hours_since_timestamp(first_timestamp)
        current_mg = caffeine_remaining(initial_mg, hours_passed, HALF_LIFE)

        remaining_seconds = max(end_time - now_unix, 0)
        remaining_hours = remaining_seconds / 3600

        st.success("Active caffeine countdown found from your Caffeine Calculator.")

    else:
        data_df = load_history_data()
        st.session_state["data_df"] = data_df

        latest_entry = get_latest_entry(data_df)

        if latest_entry is None:
            st.info("No active caffeine countdown found. Please use the Caffeine Calculator first.")
            st.stop()

        initial_mg = get_initial_caffeine(latest_entry)
        hours_passed = get_hours_since_timestamp(latest_entry["timestamp"])
        current_mg = caffeine_remaining(initial_mg, hours_passed, HALF_LIFE)
        remaining_hours = 0

    phase_name, phase_text = get_phase_info(hours_passed)

    return {
        "current_data": current_data,
        "has_active_countdown": has_active_countdown,
        "initial_mg": initial_mg,
        "current_mg": current_mg,
        "hours_passed": hours_passed,
        "remaining_hours": remaining_hours,
        "phase_name": phase_name,
        "phase_text": phase_text,
    }


def show_caffeine_status():
    status = get_caffeine_status()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Initial caffeine", f"{status['initial_mg']:.1f} mg")

    with col2:
        st.metric("Estimated current caffeine", f"{status['current_mg']:.1f} mg")

    with col3:
        st.metric("Current phase", status["phase_name"])

    with col4:
        if status["has_active_countdown"]:
            remaining_hours = status["remaining_hours"]
            st.metric("Countdown remaining", f"{int(remaining_hours)} h {int((remaining_hours % 1) * 60)} min")
        else:
            st.metric("Countdown remaining", "No active countdown")

    draw_recommendation_chart(status["hours_passed"])

    show_phase_help()

    st.success(
        f"Current interpretation: **{status['phase_name']}** — {status['phase_text']}"
    )

    if status["has_active_countdown"]:
        last_drink = status["current_data"].get("last_drink", {})
        drink_name = last_drink.get("Drink", "Selected drink")

        st.info(
            f"Last selected drink: **{drink_name}**. "
            "This recommendation page is using the saved active countdown from your Caffeine Calculator."
        )