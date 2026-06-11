"""Diabetes Risk Prediction Page — CareRisk AI."""

import streamlit as st

from utils.prediction import predict_diabetes
from utils.report_generator import generate_report
from utils.css import inject_custom_css

st.set_page_config(
    page_title="Diabetes Prediction | CareRisk AI",
    page_icon="🩸",
    layout="wide",
)
inject_custom_css()


# ---------------------------------------------------------------------------
# Helper: Professional result card (no raw model name shown)
# ---------------------------------------------------------------------------
def result_card(result: dict):
    """Render a colour-coded risk card without exposing model internals."""
    color = result["risk_color"]
    prob  = result["probability_percent"]
    level = result["risk_level"]

    # Emoji + message per level
    level_emoji = {"Low Risk": "🟢", "Medium Risk": "🟡", "High Risk": "🔴"}.get(level, "⚪")
    level_msg = {
        "Low Risk":    "Your predicted risk appears low. Keep up the healthy habits!",
        "Medium Risk": "Your predicted risk appears moderate. Consider discussing this with your doctor.",
        "High Risk":   "Your predicted risk appears elevated. We recommend consulting a healthcare professional.",
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
    # Probability progress bar
    st.progress(float(prob) / 100.0)


# ---------------------------------------------------------------------------
# Helper: Risk factor cards (human-readable explanations)
# ---------------------------------------------------------------------------
def render_risk_factors(factors: list):
    """Display top risk factors as readable explanation cards."""
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
# Helper: Ask CareRisk AI section
# ---------------------------------------------------------------------------
def render_ai_section(input_data: dict, result: dict):
    """Render the AI follow-up question assistant."""
    from utils.ai_assistant import get_ai_response

    st.markdown(
        """
        <div class="ai-section">
            <div class="ai-section-title">🤖 Ask CareRisk AI</div>
            <p style="opacity:0.8; font-size:0.95rem; margin-bottom:0.5rem;">
                Ask any question about your diabetes prediction result. Try one of these:
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
        placeholder="e.g. Why am I high risk? How can I reduce my glucose level?",
        key="diabetes_ai_question",
    )

    if st.button("💬 Get AI Explanation", key="diabetes_ai_btn", use_container_width=True):
        if not question.strip():
            st.warning("Please type a question before clicking the button.")
        else:
            with st.spinner("CareRisk AI is thinking..."):
                answer = get_ai_response(
                    question=question,
                    disease_type="Diabetes",
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
st.markdown('<div class="section-title">🩸 Diabetes Risk Screening</div>', unsafe_allow_html=True)
st.caption("Enter patient physiological data to generate a risk prediction.")

with st.form("diabetes_form"):
    st.markdown("##### 👤 Patient Diagnostics")
    c1, c2 = st.columns(2)
    with c1:
        Pregnancies          = st.number_input("Pregnancies", min_value=0, max_value=20, value=1,
                                               help="Number of times pregnant")
        Glucose              = st.number_input("Glucose Concentration (mg/dL)", min_value=0.0,
                                               max_value=300.0, value=120.0,
                                               help="2-hour oral glucose tolerance test value")
        BloodPressure        = st.number_input("Diastolic Blood Pressure (mm Hg)", min_value=0.0,
                                               max_value=200.0, value=70.0)
        SkinThickness        = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0.0,
                                               max_value=100.0, value=20.0)
    with c2:
        Insulin              = st.number_input("2-Hour Serum Insulin (µU/mL)", min_value=0.0,
                                               max_value=900.0, value=80.0)
        BMI                  = st.number_input("Body Mass Index (BMI)", min_value=0.0,
                                               max_value=80.0, value=28.0)
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0,
                                                   max_value=3.0, value=0.45,
                                                   help="Genetic family history likelihood score")
        Age                  = st.number_input("Age (years)", min_value=1, max_value=120, value=35)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Run Diabetes Risk Analysis", use_container_width=True)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if submitted:
    st.session_state["diabetes_input"] = {
        "Pregnancies": Pregnancies,
        "Glucose": Glucose,
        "BloodPressure": BloodPressure,
        "SkinThickness": SkinThickness,
        "Insulin": Insulin,
        "BMI": BMI,
        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
        "Age": Age,
    }
    st.session_state["diabetes_result"] = predict_diabetes(st.session_state["diabetes_input"])

if "diabetes_result" in st.session_state:
    input_data = st.session_state["diabetes_input"]
    result = st.session_state["diabetes_result"]

    if "error" in result:
        st.warning(result["error"])
        st.info("Run: `python -m utils.model_training --disease diabetes` after adding `data/diabetes.csv`.")
    else:
        st.markdown('<div class="section-title">📊 Analysis Result</div>', unsafe_allow_html=True)

        # --- Risk card full-width ---
        result_card(result)

        # --- Risk factors | PDF download ---
        col1, col2 = st.columns([1.3, 1])

        with col1:
            st.subheader("📌 Key Risk Factors")
            render_risk_factors(result.get("top_factors", []))

        with col2:
            st.subheader("📄 Download Report")
            # Safe PDF generation — don't crash if it fails
            try:
                pdf_bytes = generate_report(
                    patient_data=input_data,
                    disease_type="Diabetes",
                    prediction=result["prediction"],
                    probability=result["probability"],
                    risk_level=result["risk_level"],
                    top_factors=result["top_factors"],
                )
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="diabetes_risk_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

            # Technical details in a collapsed expander (hidden from normal users)
            with st.expander("🔧 Technical Details"):
                st.write(f"**Model:** {result['model_used']}")
                st.write(f"**Raw Probability:** {result['probability']:.4f}")
                st.write(f"**Prediction Class:** {result['prediction']} ({'Positive' if result['prediction'] else 'Negative'})")
                st.write(f"**Features used:** {len(result.get('top_factors', []))}")

        # --- AI Assistant ---
        render_ai_section(input_data, result)

        # --- Disclaimer ---
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
