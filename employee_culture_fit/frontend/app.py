import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000/predict_all"

st.set_page_config(page_title="Culture Fit Analyzer", layout="wide")

# ---------------------------- CSS: SAPPHIRE & SILVER THEME ----------------------------
st.markdown("""
<style>

body {
    background-color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F8FAFC !important;
}

.glass-card {
    background: rgba(255, 255, 255, 0.82);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid rgba(180, 187, 196, 0.45);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 30px rgba(15, 76, 129, 0.10);
}

.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #CBD5E1;
    text-align: center;
    box-shadow: 0px 6px 14px rgba(15, 76, 129, 0.08);
}

.metric-title {
    font-size: 0.85rem;
    color: #64748B;
    text-transform: uppercase;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0F4C81;
}

.tag {
    display: inline-block;
    background: #E0E7EF;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9rem;
    color: #0F4C81;
    border: 1px solid #CBD5E1;
}

.title-main {
    font-size: 2.2rem;
    font-weight: 750;
    color: #0F4C81;
}

.subtitle {
    color: #475569;
    font-size: 1.05rem;
}

hr {
    border: none;
    border-top: 1px solid #CBD5E1;
    margin-top: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------- HEADER ----------------------------
st.markdown("""
<div class="title-main">👥 Employee Culture Fit Analyzer</div>
<p class="subtitle">
A Deloitte-style behavioral analytics dashboard that evaluates culture fit, interpersonal compatibility, and ideal team placement.
</p>
""", unsafe_allow_html=True)

st.write("")
left, right = st.columns([1.1, 1])

# ---------------------------- LEFT PANEL ----------------------------
with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📄 Candidate Profile")

    c1, c2, c3 = st.columns(3)
    with c1:
        openness = st.slider("Openness", 0.2, 0.95, 0.7, 0.01)
        extraversion = st.slider("Extraversion", 0.2, 0.95, 0.6, 0.01)
    with c2:
        conscientiousness = st.slider("Conscientiousness", 0.2, 0.95, 0.75, 0.01)
        agreeableness = st.slider("Agreeableness", 0.2, 0.95, 0.7, 0.01)
    with c3:
        neuroticism = st.slider("Neuroticism", 0.1, 0.9, 0.35, 0.01)

    st.markdown("---")
    st.subheader("💼 Workstyle Preferences")

    w1, w2, w3 = st.columns(3)
    with w1: pref_pace = st.selectbox("Work Pace", ["Slow", "Balanced", "Fast"])
    with w2: pref_comm = st.selectbox("Communication", ["Direct", "Neutral", "Indirect"])
    with w3: pref_setting = st.selectbox("Work Setting", ["Remote", "Hybrid", "Office"])

    st.markdown("---")
    st.subheader("💡 Values Alignment (1–10)")

    v1, v2, v3, v4 = st.columns(4)
    with v1: val_innov = st.slider("Innovation", 1, 10, 8)
    with v2: val_team = st.slider("Teamwork", 1, 10, 9)
    with v3: val_lead = st.slider("Leadership", 1, 10, 7)
    with v4: val_ethics = st.slider("Ethics", 1, 10, 9)

    analyze = st.button("🔍 Analyze Candidate", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------- RIGHT PANEL ----------------------------
with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Candidate Insights")

    if analyze:

        payload = {
            "Openness": openness,
            "Conscientiousness": conscientiousness,
            "Extraversion": extraversion,
            "Agreeableness": agreeableness,
            "Neuroticism": neuroticism,
            "Pref_Work_Pace": pref_pace,
            "Pref_Communication": pref_comm,
            "Pref_Work_Setting": pref_setting,
            "Value_Innovation": val_innov,
            "Value_Teamwork": val_team,
            "Value_Leadership": val_lead,
            "Value_Ethics": val_ethics,
        }

        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            r = res.json()


            score = r["culture_fit_score"]
            conflict = r["conflict_risk"]
            team = r["recommended_team"]

            m1, m2 = st.columns(2)

            # -------- Culture Fit Score Gauge --------
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Culture Fit Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#0F4C81"},
                    "steps": [
                        {"range": [0, 40], "color": "#FECACA"},
                        {"range": [40, 70], "color": "#FDE68A"},
                        {"range": [70, 100], "color": "#BBF7D0"},
                    ],
                },
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))

            with m1:
                st.plotly_chart(fig_gauge, use_container_width=True)

            # -------- Conflict Risk Metric --------
            with m2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-title">Conflict Risk</div>', unsafe_allow_html=True)
                emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[conflict]
                st.markdown(f'<div class="metric-value">{emoji} {conflict}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # -------- Recommended Team Tag --------
            st.write("")
            st.markdown("### 🎯 Recommended Team Fit")
            st.markdown(f"<span class='tag'>{team}</span>", unsafe_allow_html=True)

            # -------- Personality Radar Chart --------
            st.markdown("---")
            st.subheader("📈 Personality Profile Radar")

            traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
            values = [openness, conscientiousness, extraversion, agreeableness, neuroticism]

            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=traits + [traits[0]],
                fill='toself',
                line_color="#0F4C81"
            ))
            radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0.2, 1]),
                ),
                showlegend=False,
                height=350
            )

            st.plotly_chart(radar, use_container_width=True)

            # -------- Interpretation --------
            st.markdown("---")
            st.subheader("📝 Interpretation Summary")

            insights = []

            if score >= 75:
                insights.append("✔ Strong cultural alignment; highly compatible with organizational values.")
            elif score >= 55:
                insights.append("✔ Moderate fit; onboarding and mentoring will accelerate integration.")
            else:
                insights.append("⚠️ Low cultural match; may require structured guidance.")

            if conflict == "High":
                insights.append("⚠️ High conflict potential—role restructuring or coaching advised.")
            elif conflict == "Medium":
                insights.append("⚠️ Moderate conflict risk—suited for stable, process-driven teams.")
            else:
                insights.append("✔ Low conflict risk—smooth interpersonal compatibility expected.")

            for item in insights:
                st.markdown(f"- {item}")

        else:
            st.error("API Response Error")

    else:
        st.info("Fill the left panel and click **Analyze Candidate** to view insights.")

    st.markdown("</div>", unsafe_allow_html=True)
