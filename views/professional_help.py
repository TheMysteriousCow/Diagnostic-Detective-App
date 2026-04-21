import streamlit as st

st.set_page_config(page_title="Professional Help", layout="wide")

# -----------------------------
# PAGE STYLE
# -----------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f6f4;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .help-title {
            text-align: center;
            font-size: 5rem;
            font-weight: 800;
            color: #6b4a3b;
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .help-subtitle {
            text-align: center;
            font-size: 1.15rem;
            color: #6b7280;
            margin-bottom: 2.5rem;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #6b4a3b;
            margin-top: 0.4rem;
            margin-bottom: 1rem;
        }

        .intro-box {
            background: linear-gradient(135deg, #eef5ff 0%, #f7fbff 100%);
            border: 1px solid #d7e6fb;
            border-radius: 22px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1.3rem;
            color: #334155;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
        }

        .urgent-box {
            background: linear-gradient(135deg, #fff1f2 0%, #fff7f7 100%);
            border: 1px solid #fecdd3;
            border-radius: 22px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 2rem;
            color: #7f1d1d;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
        }

        .card {
            background: white;
            border-radius: 24px;
            padding: 1.4rem 1.3rem 1.25rem 1.3rem;
            border: 1px solid #ece7e3;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.05);
            min-height: 390px;
            margin-bottom: 1rem;
        }

        .card-tag {
            display: inline-block;
            font-size: 0.82rem;
            font-weight: 700;
            color: #6b7280;
            background-color: #f4f4f5;
            border-radius: 999px;
            padding: 0.28rem 0.7rem;
            margin-bottom: 0.85rem;
        }

        .card-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: #6b4a3b;
            margin-bottom: 0.25rem;
        }

        .card-role {
            font-size: 1rem;
            font-weight: 600;
            color: #475569;
            margin-bottom: 1rem;
        }

        .card-text {
            font-size: 1rem;
            color: #4b5563;
            line-height: 1.7;
            margin-bottom: 1rem;
        }

        .note-text {
            font-size: 0.95rem;
            color: #6b7280;
            line-height: 1.6;
            margin-top: 1.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="help-title">Professional Help</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="help-subtitle">Find trusted support and quick access to professional help when you need it.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# INTRO
# -----------------------------
st.markdown(
    """
    <div class="intro-box">
        <strong>This page is here for support.</strong><br>
        If caffeine, stress, sleep problems, inner unrest, nutrition topics or your general wellbeing feel too much,
        professional guidance can help you sort things calmly and step by step.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="urgent-box">
        <strong>Important:</strong> For urgent or serious medical concerns, use the <strong>AERZTEFON</strong>.
        It is available <strong>24 hours, 365 days</strong> and helps with medical and dental emergencies that are
        <strong>not life-threatening</strong>. In case of <strong>acute danger to life</strong>, call <strong>144 immediately</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Professional help & support</div>', unsafe_allow_html=True)

# -----------------------------
# CARDS
# -----------------------------
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-tag">Holistic support</div>
            <div class="card-title">HER. MOTI☽N</div>
            <div class="card-role">Valerie</div>
            <div class="card-text">
                A supportive space for people who want to reconnect with themselves more deeply.
                HER. MOTI☽N offers holistic 1:1 support with a strong focus on body awareness,
                emotional wellbeing, inner balance and personal growth.
            </div>
            <div class="card-text">
                Valerie presents herself is a therapist and mentor. Her work includes
                body-based and holistic approaches, and she works in naturopathy and energy-based support. The offer has a visible focus on women,
                but can still be inspiring for anyone looking for gentle, more holistic guidance.
            </div>
            <div class="card-text">
                This can be a good option if you feel that your caffeine habits are connected to stress,
                overwhelm, nervous system dysregulation, low energy, hormonal imbalance or the wish to
                take better care of yourself in a broader way.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("Visit HER. MOTI☽N", "https://www.hermotion.space/", use_container_width=True)

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-tag">Nutrition & holistic health</div>
            <div class="card-title">Sunima</div>
            <div class="card-role">Martina Zulauf</div>
            <div class="card-text">
                Sunima may be especially interesting if you are looking for a calm, more holistic approach
                to wellbeing with an additional nutrition background.
            </div>
            <div class="card-text">
                Martina Zulauf is a Reiki master and has training in
                <strong>orthomolecular medicine</strong>, as a <strong>certified advisor for holistic health</strong>,
                and as a <strong>certified fasting instructor</strong>.
                This combination can be valuable for people who want support around energy, lifestyle,
                nourishment and general health habits.
            </div>
            <div class="card-text">
                This can be a fitting place to start if you want guidance beyond “just stop drinking caffeine” and
                instead want to look at your body, recovery, daily rhythm and nutrition in a more complete way.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("Visit Sunima", "https://www.sunima.ch/", use_container_width=True)

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-tag">Urgent medical support</div>
            <div class="card-title">AERZTEFON</div>
            <div class="card-role">Medical emergency helpline</div>
            <div class="card-text">
                AERZTEFON is the right contact for <strong>serious medical concerns</strong>, strong symptoms,
                major uncertainty, or situations where you need fast professional medical orientation.
            </div>
            <div class="card-text">
                According to the official website, AERZTEFON is available <strong>24/7</strong> and helps with
                <strong>non-life-threatening medical and dental emergencies</strong>. Their team provides a medical
                assessment and helps connect people to the right next step in care.
            </div>
            <div class="card-text">
                Use this option for example if symptoms feel intense, frightening or unusual.
                <strong>If there is acute danger to life, call 144 immediately.</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("Call / visit AERZTEFON", "https://www.aerztefon.ch/", use_container_width=True)

# -----------------------------
# FOOTNOTE
# -----------------------------
st.markdown(
    """
    <div class="note-text">
        This page is meant as supportive orientation and not as a diagnosis page.
        If symptoms are severe, rapidly worsening, or feel medically unsafe, seek urgent medical help.
    </div>
    """,
    unsafe_allow_html=True,
)