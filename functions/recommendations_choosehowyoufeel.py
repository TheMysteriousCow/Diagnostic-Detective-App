import streamlit as st


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


DETAILS = {
    "Peak": {
        "title": "Peak",
        "intro": "Your caffeine effect is currently high. This is the phase in which alertness and stimulation are strongest.",
        "tips": [
            "Avoid additional caffeine right now.",
            "Drink water to stay hydrated.",
            "Use this phase for focused work, but do not overdo it.",
            "If you feel shaky, take a short break and eat something light."
        ],
        "warning": "Too much caffeine during the peak phase can increase nervousness, inner restlessness and heartbeat."
    },
    "Increase": {
        "title": "Increase",
        "intro": "Your caffeine effect is currently building up. The peak is usually reached after about 45 minutes.",
        "tips": [
            "Do not take more caffeine too quickly.",
            "Wait until the full effect arrives.",
            "Drink water alongside caffeine.",
            "Notice whether your body feels calm, energized or overstimulated."
        ],
        "warning": "Taking more caffeine during the increase phase can make the later peak stronger than expected."
    },
    "Crash": {
        "title": "Crash",
        "intro": "The caffeine effect is going down. Some people feel tired, unfocused, low in energy or slightly irritable during this phase.",
        "tips": [
            "Drink water first and give your body a short pause.",
            "Eat something balanced instead of immediately reaching for more caffeine.",
            "Go outside or move gently for a few minutes.",
            "Avoid a second large caffeine dose if it is already late in the day."
        ],
        "warning": "Using caffeine repeatedly to escape a crash can create a cycle of stimulation followed by stronger tiredness later."
    },
    "I can't fall asleep": {
        "title": "I can't fall asleep",
        "intro": "There may still be caffeine in your body, especially if you consumed it late in the day.",
        "tips": [
            "Do not take more caffeine today.",
            "Avoid screens and bright light before sleep.",
            "Drink water, but not too much right before bed.",
            "Try a calm environment and slow breathing."
        ],
        "warning": "If sleep problems happen often, reduce caffeine in the afternoon and evening."
    },
    "I feel tired": {
        "title": "I feel tired",
        "intro": "Your caffeine effect may already be dropping. This can happen after the stimulating phase wears off.",
        "tips": [
            "Drink water first.",
            "Eat a balanced snack.",
            "Get fresh air or move for a few minutes.",
            "Avoid automatically taking more caffeine immediately."
        ],
        "warning": "Repeated caffeine use against tiredness can lead to a cycle of short-term stimulation and later tiredness."
    },
    "I feel anxious": {
        "title": "I feel anxious",
        "intro": "High caffeine levels can increase nervousness, restlessness or tension.",
        "tips": [
            "Stop caffeine for the rest of the day.",
            "Drink water slowly.",
            "Sit down and breathe slowly and deeply.",
            "Reduce other stimulants if possible."
        ],
        "warning": "If symptoms are strong or unusual, professional medical advice may be necessary."
    },
    "I can't concentrate": {
        "title": "I can't concentrate",
        "intro": "Too little or too much caffeine can both affect concentration.",
        "tips": [
            "Check whether you are in a crash phase or overstimulated.",
            "Drink water and take a short movement break.",
            "Work in short blocks instead of forcing long focus periods.",
            "Avoid taking more caffeine too quickly."
        ],
        "warning": "Poor concentration is not always caused by caffeine. Sleep, stress and food intake also matter."
    },
    "Recovery": {
        "title": "Recovery",
        "intro": "Your body is slowly returning to a calmer state. The caffeine effect is lower now.",
        "tips": [
            "Drink water and listen to your natural energy level.",
            "Fresh air, food or rest may help more than another coffee.",
            "Use this phase to return to a more balanced rhythm.",
            "Avoid taking caffeine automatically just because the effect is fading."
        ],
        "warning": "If you often rely on caffeine again during recovery, it can become a repeating cycle."
    },
    "Stomach discomfort or acidity": {
        "title": "Stomach discomfort or acidity",
        "intro": "Caffeine can irritate the stomach in some people and may feel worse if you drink it on an empty stomach.",
        "tips": [
            "Avoid more caffeine for now, especially coffee or energy drinks.",
            "Drink water slowly.",
            "Eat something mild, for example bread, rice, banana or oatmeal.",
            "Avoid very spicy, acidic or fatty foods for the moment.",
            "Notice whether certain caffeine sources cause more discomfort than others."
        ],
        "warning": "If stomach pain is strong, keeps coming back, or is combined with vomiting, blood, chest pain or severe burning, seek medical advice."
    },
    "I have a headache": {
        "title": "I have a headache",
        "intro": "Headaches can have many causes. With caffeine, they may be linked to dehydration, too much caffeine, caffeine withdrawal, stress or lack of sleep.",
        "tips": [
            "Drink water slowly and rest your eyes for a few minutes.",
            "Eat something if you have not eaten enough.",
            "Avoid taking more caffeine immediately unless you know caffeine withdrawal is likely.",
            "Move gently or get fresh air if it feels helpful.",
            "Track whether headaches happen after high caffeine intake or when you skip caffeine."
        ],
        "warning": "Seek medical help if the headache is sudden and severe, unusual for you, follows an injury, or comes with fever, confusion, weakness, vision problems or chest pain."
    },
    "I am training soon or doing sports": {
        "title": "I am training soon or doing sports",
        "intro": "Caffeine can support alertness and performance for some people, but too much can also increase nervousness, stomach discomfort or a racing heartbeat during exercise.",
        "tips": [
            "Avoid taking extra caffeine if you already feel shaky, anxious or overstimulated.",
            "Drink water before and during training.",
            "Do not train after a large caffeine dose if your stomach feels sensitive.",
            "Keep caffeine moderate and avoid experimenting with high doses.",
            "After training, focus on hydration, food and recovery."
        ],
        "warning": "Stop exercising and seek help if you feel chest pain, faintness, severe shortness of breath, irregular heartbeat or unusual strong symptoms."
    },
}


def show_selected_detail():
    selected_detail = st.session_state["recommendation_detail"]

    if selected_detail in DETAILS:
        detail = DETAILS[selected_detail]

        show_detail_page(
            title=detail["title"],
            intro=detail["intro"],
            tips=detail["tips"],
            warning=detail["warning"]
        )

        st.stop()


def show_choose_how_you_feel():
    st.markdown("### Choose how you feel")

    col_a, col_b = st.columns(2)

    with col_a:
        for label in [
            "Increase",
            "Peak",
            "Crash",
            "I feel tired",
            "I feel anxious",
            "Stomach discomfort or acidity",
        ]:
            if st.button(label, use_container_width=True):
                st.session_state["recommendation_detail"] = label
                st.rerun()

    with col_b:
        for label in [
            "I can't fall asleep",
            "I can't concentrate",
            "I have a headache",
            "I am training soon or doing sports",
            "Recovery",
        ]:
            if st.button(label, use_container_width=True):
                st.session_state["recommendation_detail"] = label
                st.rerun()