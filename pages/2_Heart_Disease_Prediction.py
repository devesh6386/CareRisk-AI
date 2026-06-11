"""Heart Disease Risk Prediction Page — CareRisk AI."""

import streamlit as st

from utils.prediction import predict_heart
from utils.report_generator import generate_report
from utils.css import inject_custom_css

st.set_page_config(
    page_title="Heart Disease Prediction | CareRisk AI",
    page_icon="❤️",
    layout="wide",
)
inject_custom_css()


# ---------------------------------------------------------------------------
# Helper: Professional result card
# ---------------------------------------------------------------------------
def result_card(result: dict):
    """Render a colour-coded risk card without exposing model internals."""
    color = result["risk_color"]
    prob  = result["probability_percent"]
    level = result["risk_level"]

    level_emoji = {"Low Risk": "🟢", "Medium Risk": "🟡", "High Risk": "🔴"}.get(level, "⚪")
    level_msg = {
        "Low Risk":    "Your predicted cardiovascular risk appears low. Maintain your healthy lifestyle!",
        "Medium Risk": "Your predicted cardiovascular risk appears moderate. A doctor visit is advisable.",
        "High Risk":   "Your predicted cardiovascular risk appears elevated. Please consult a healthcare professional.",
    }.get(level, "")

    st.markdown(
        f"""
        <div class="risk-card" style="border-left: 8px solid {color} !important;">
            <h2 style="color: {color} !important;">{level_emoji} {level}</h2>
            <p>{level_msg}</p>
            <p style="font-size:1rem; opacity:0.75; margin-top:0.75rem !important;">
                Model confidence: <strong>{prob}%</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(float(prob) / 100.0)


# ---------------------------------------------------------------------------
# Helper: Risk factor cards
# ---------------------------------------------------------------------------
def render_risk_factors(factors: list):
    if not factors:
        st.info("Feature importance is not available for this model.")
        return

    for i, f in enumerate(factors, 1):
        explanation = f.get("explanation") or f.get("feature", "Unknown factor")
        st.markdown(
            f"""
            <div class="factor-card">
                <span class="factor-number">{i}</span>
                <span class="factor-text">{explanation}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Helper: AI assistant section
# ---------------------------------------------------------------------------
def render_ai_section(input_data: dict, result: dict):
    from utils.ai_assistant import get_ai_response

    st.markdown(
        """
        <div class="ai-section">
            <div class="ai-section-title">🤖 Ask CareRisk AI</div>
            <p style="opacity:0.8; font-size:0.95rem; margin-bottom:0.5rem;">
                Ask any question about your heart disease risk result. Try one of these:
            </p>
            <div class="question-chips">
                <span class="question-chip">💬 Why am I high risk?</span>
                <span class="question-chip">📊 Which factors affected my result?</span>
                <span class="question-chip">🔽 How can I reduce my risk?</span>
                <span class="question-chip">🗣️ Explain my result in simple words.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Your question:",
        placeholder="e.g. What does my cholesterol value mean for my heart?",
        key="heart_ai_question",
    )

    if st.button("💬 Get AI Explanation", key="heart_ai_btn", use_container_width=True):
        if not question.strip():
            st.warning("Please type a question before clicking the button.")
        else:
            with st.spinner("CareRisk AI is thinking..."):
                answer = get_ai_response(
                    question=question,
                    disease_type="Heart Disease",
                    patient_data=input_data,
                    prediction_result=result["prediction"],
                    probability=result["probability"],
                    risk_level=result["risk_level"],
                    top_factors=result["top_factors"],
                )
            st.markdown('<div class="ai-response-box">', unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown('</div>', unsafe_allow_html=True)



# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">❤️ Heart Disease Risk Screening</div>', unsafe_allow_html=True)
st.caption("Provide cardiovascular clinical parameters to generate a risk prediction.")

with st.form("heart_form"):
    st.markdown("##### 👤 Patient Diagnostics")
    c1, c2, c3 = st.columns(3)

    with c1:
        age      = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
        sex      = st.selectbox("Sex", options=[0, 1],
                                format_func=lambda x: "Female (0)" if x == 0 else "Male (1)")
        cp       = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3],
                                format_func=lambda x: {
                                    0: "0 – Typical Angina",
                                    1: "1 – Atypical Angina",
                                    2: "2 – Non-anginal Pain",
                                    3: "3 – Asymptomatic",
                                }[x])
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=60, max_value=250, value=130)
        chol     = st.number_input("Serum Cholesterol (mg/dL)", min_value=80, max_value=700, value=240)

    with c2:
        fbs     = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=[0, 1],
                               format_func=lambda x: "No – False (0)" if x == 0 else "Yes – True (1)")
        restecg = st.selectbox("Resting Electrocardiographic Results", options=[0, 1, 2],
                               format_func=lambda x: {
                                   0: "0 – Normal",
                                   1: "1 – ST-T Wave Abnormality",
                                   2: "2 – Left Ventricular Hypertrophy",
                               }[x])
        thalach = st.number_input("Maximum Heart Rate Achieved (bpm)", min_value=60, max_value=250, value=150)
        exang   = st.selectbox("Exercise-Induced Angina", options=[0, 1],
                               format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")

    with c3:
        oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0,
                                  value=1.0, step=0.1,
                                  help="ST depression induced by exercise relative to rest")
        slope   = st.selectbox("Slope of Peak Exercise ST Segment", options=[0, 1, 2],
                               format_func=lambda x: {
                                   0: "0 – Upsloping",
                                   1: "1 – Flat",
                                   2: "2 – Downsloping",
                               }[x])
        ca      = st.selectbox("Major Vessels Colored by Fluoroscopy (0–4)", options=[0, 1, 2, 3, 4])
        thal    = st.selectbox("Thalassemia (thal)", options=[0, 1, 2, 3],
                               format_func=lambda x: {
                                   0: "0 – Unknown",
                                   1: "1 – Normal",
                                   2: "2 – Fixed Defect",
                                   3: "3 – Reversible Defect",
                               }[x])

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Run Heart Disease Analysis", use_container_width=True)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if submitted:
    st.session_state["heart_input"] = {
        "age": age, "sex": sex, "cp": cp, "trestbps": trestbps,
        "chol": chol, "fbs": fbs, "restecg": restecg, "thalach": thalach,
        "exang": exang, "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal,
    }
    st.session_state["heart_result"] = predict_heart(st.session_state["heart_input"])

if "heart_result" in st.session_state:
    input_data = st.session_state["heart_input"]
    result = st.session_state["heart_result"]

    if "error" in result:
        st.warning(result["error"])
        st.info("Run: `python -m utils.model_training --disease heart` after adding `data/heart.csv`.")
    else:
        st.markdown('<div class="section-title">📊 Analysis Result</div>', unsafe_allow_html=True)

        result_card(result)

        col1, col2 = st.columns([1.3, 1])

        with col1:
            st.subheader("📌 Key Risk Factors")
            render_risk_factors(result.get("top_factors", []))

        with col2:
            st.subheader("📄 Download Report")
            try:
                pdf_bytes = generate_report(
                    patient_data=input_data,
                    disease_type="Heart Disease",
                    prediction=result["prediction"],
                    probability=result["probability"],
                    risk_level=result["risk_level"],
                    top_factors=result["top_factors"],
                )
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="heart_disease_risk_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

            with st.expander("🔧 Technical Details"):
                st.write(f"**Model:** {result['model_used']}")
                st.write(f"**Raw Probability:** {result['probability']:.4f}")
                st.write(f"**Prediction Class:** {result['prediction']} ({'Positive' if result['prediction'] else 'Negative'})")
                st.write(f"**Features used:** {len(result.get('top_factors', []))}")

        render_ai_section(input_data, result)

        st.markdown(
            """
            <div class="disclaimer-box">
                <p>⚠️ <strong>Medical Disclaimer:</strong> This prediction is generated by an ML model and
                is not a medical diagnosis. It does not substitute for professional medical advice.
                Always consult a qualified healthcare professional for medical decisions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
