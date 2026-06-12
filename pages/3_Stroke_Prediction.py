"""Stroke Risk Prediction Page — CareRisk AI."""

import streamlit as st
from utils.prediction import predict_stroke
from utils.report_generator import generate_report
from utils.css import inject_custom_css, render_sidebar

st.set_page_config(
    page_title="Stroke Prediction | CareRisk AI",
    page_icon="🧠",
    layout="wide",
)

# Inject custom CSS and render unified sidebar
inject_custom_css()
render_sidebar()


# ---------------------------------------------------------------------------
# Helper: Professional result card (no raw model name shown)
# ---------------------------------------------------------------------------
def result_card(result: dict):
    """Render a colour-coded risk card without exposing model internals."""
    color = result["risk_color"]
    prob = result["probability_percent"]
    level = result["risk_level"]

    level_emoji = {"Low Risk": "🟢", "Medium Risk": "🟡", "High Risk": "🔴"}.get(level, "⚪")
    level_msg = {
        "Low Risk": "Your predicted risk appears low. Keep up the healthy habits!",
        "Medium Risk": "Your predicted risk appears moderate. Consider discussing this with your doctor.",
        "High Risk": "Your predicted risk appears elevated. We recommend consulting a healthcare professional.",
    }.get(level, "")

    st.markdown(
        f"""
        <div class="risk-card" style="border-left: 8px solid {color} !important;">
            <h2 style="color: {color} !important; margin: 0 0 0.5rem 0;">{level_emoji} {level}</h2>
            <p>{level_msg}</p>
            <p style="font-size:1.05rem; opacity:0.95; margin: 0.75rem 0 0.25rem 0 !important; font-weight: 600;">
                Model Confidence: {prob}%
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
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
                Ask any question about your stroke risk result. Try one of these:
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
        placeholder="e.g. How does hypertension affect my stroke risk?",
        key="stroke_ai_question",
    )

    if st.button("💬 Get AI Explanation", key="stroke_ai_btn", use_container_width=True):
        if not question.strip():
            st.warning("Please type a question before clicking the button.")
        else:
            with st.spinner("CareRisk AI is thinking..."):
                answer = get_ai_response(
                    question=question,
                    disease_type="Stroke",
                    patient_data=input_data,
                    prediction_result=result["prediction"],
                    probability=result["probability"],
                    risk_level=result["risk_level"],
                    top_factors=result["top_factors"],
                )
            st.markdown('<div class="ai-response-box">', unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown('</div>', unsafe_allow_html=True)


# ===========================================================================
# 2-Column Desktop Page Layout
# ===========================================================================
st.markdown('<div class="section-title">🧠 Stroke Risk Screening</div>', unsafe_allow_html=True)

col_form, col_result = st.columns([1, 1.25])

with col_form:
    with st.form("stroke_form"):
        st.markdown("##### 👤 Demographic & Clinical Parameters")
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        age = st.number_input("Age (years)", min_value=0.0, max_value=120.0,
                              value=45.0, step=1.0)
        hypertension = st.selectbox("Hypertension Status", options=[0, 1],
                                     format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")
        heart_disease = st.selectbox("Heart Disease History", options=[0, 1],
                                     format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")
        ever_married = st.selectbox("Ever Married?", options=["Yes", "No"])
        work_type = st.selectbox("Work Type",
                                  options=["Private", "Self-employed", "Govt_job",
                                           "children", "Never_worked"])
        Residence_type = st.selectbox("Residence Type", options=["Urban", "Rural"])
        avg_glucose_level = st.number_input("Average Glucose Level (mg/dL)",
                                            min_value=40.0, max_value=350.0,
                                            value=100.0, step=0.1)
        bmi = st.number_input("Body Mass Index (BMI)", min_value=5.0,
                               max_value=100.0, value=25.0, step=0.1)
        smoking_status = st.selectbox(
            "Smoking Status",
            options=["formerly smoked", "never smoked", "smokes", "Unknown"],
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍 Run Stroke Risk Analysis", use_container_width=True)

# Process form submission
if submitted:
    st.session_state["stroke_input"] = {
        "gender": gender, "age": age, "hypertension": hypertension,
        "heart_disease": heart_disease, "ever_married": ever_married,
        "work_type": work_type, "Residence_type": Residence_type,
        "avg_glucose_level": avg_glucose_level, "bmi": bmi, "smoking_status": smoking_status,
    }
    st.session_state["stroke_result"] = predict_stroke(st.session_state["stroke_input"])

# Result display in right column
with col_result:
    if "stroke_result" in st.session_state:
        input_data = st.session_state["stroke_input"]
        result = st.session_state["stroke_result"]

        if "error" in result:
            st.warning(result["error"])
            st.info("Run: `python -m utils.model_training --disease stroke` after adding `data/stroke.csv`.")
        else:
            st.markdown("### 📊 Diagnostic Risk Assessment")

            # 1. Risk level card + Progress bar
            result_card(result)
            st.markdown("<br>", unsafe_allow_html=True)

            # 2. Key risk factors
            st.markdown("##### 📌 Top Risk Contributing Factors")
            render_risk_factors(result.get("top_factors", []))
            st.markdown("<br>", unsafe_allow_html=True)

            # 3. Actions (PDF Report + Tech details)
            c_pdf, c_tech = st.columns([1.5, 1])
            with c_pdf:
                try:
                    pdf_bytes = generate_report(
                        patient_data=input_data,
                        disease_type="Stroke",
                        prediction=result["prediction"],
                        probability=result["probability"],
                        risk_level=result["risk_level"],
                        top_factors=result["top_factors"],
                    )
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name="stroke_risk_report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
            with c_tech:
                with st.expander("🔧 Model Details"):
                    st.write(f"**Model:** {result['model_used']}")
                    st.write(f"**Raw Probability:** {result['probability']:.4f}")
                    st.write(f"**Prediction Class:** {result['prediction']}")

            # 4. Chatbot Q&A
            render_ai_section(input_data, result)

            # 5. Medical Disclaimer
            st.markdown(
                """
                <div class="disclaimer-box">
                    <p>⚠️ <strong>Important Medical Disclaimer:</strong> CareRisk AI predictions are probabilistic and generated using machine learning. They do not substitute for professional medical consults. Please discuss these values with your primary care provider.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        # Placeholder when no screening has run
        st.markdown(
            """
            <div class="risk-card" style="border-left: 6px solid var(--blue-color) !important; min-height: 480px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 2.5rem !important;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: var(--teal-color);">Awaiting Diagnostics</h3>
                <p style="color: #64748b; font-size: 0.98rem; max-width: 320px; margin: 0.5rem auto 0 auto; line-height: 1.5;">
                    Provide patient metrics in the form on the left and submit to view risk level, SHAP factor explanations, PDF reports, and enable the AI assistant.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
