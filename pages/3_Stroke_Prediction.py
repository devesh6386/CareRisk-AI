import streamlit as st
import pandas as pd

from utils.prediction import predict_stroke
from utils.report_generator import generate_report
from utils.css import inject_custom_css

st.set_page_config(page_title="Stroke Prediction | CareRisk AI", page_icon="🧠", layout="wide")
inject_custom_css()


def result_card(result):
    color = result["risk_color"]
    prob = result['probability_percent']
    st.markdown(
        f"""
        <div class="risk-card" style="border-left: 8px solid {color} !important;">
            <h2 style="color: {color} !important; margin: 0 0 0.5rem 0;">{result['risk_level']} Risk Profile</h2>
            <p style="margin: 0.5rem 0 !important; font-size: 1.15rem;">Risk Probability: <strong>{prob}%</strong></p>
            <p style="margin: 0.5rem 0 !important; font-size: 1.15rem;">Active Estimator: <strong>{result['model_used']}</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(float(prob) / 100.0)


st.markdown('<div class="section-title">🧠 Stroke Risk Screening</div>', unsafe_allow_html=True)
st.caption("Provide demographic and clinical attributes to assess stroke risk probability.")

with st.form("stroke_form"):
    st.markdown("##### 👤 Demographic & Clinical Parameters")
    c1, c2 = st.columns(2)

    with c1:
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        age = st.number_input("Age (years)", min_value=0.0, max_value=120.0, value=45.0, step=1.0)
        hypertension = st.selectbox("Hypertension Status", options=[0, 1], format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")
        heart_disease = st.selectbox("Heart Disease History", options=[0, 1], format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")
        ever_married = st.selectbox("Ever Married?", options=["Yes", "No"])

    with c2:
        work_type = st.selectbox("Work Type", options=["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
        Residence_type = st.selectbox("Residence Type", options=["Urban", "Rural"])
        avg_glucose_level = st.number_input("Average Glucose Level (mg/dL)", min_value=40.0, max_value=350.0, value=100.0, step=0.1)
        bmi = st.number_input("Body Mass Index (BMI)", min_value=5.0, max_value=100.0, value=25.0, step=0.1)
        smoking_status = st.selectbox(
            "Smoking Status",
            options=["formerly smoked", "never smoked", "smokes", "Unknown"],
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Run Stroke Risk Analysis", use_container_width=True)

if submitted:
    input_data = {
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "ever_married": ever_married,
        "work_type": work_type,
        "Residence_type": Residence_type,
        "avg_glucose_level": avg_glucose_level,
        "bmi": bmi,
        "smoking_status": smoking_status,
    }

    result = predict_stroke(input_data)

    if "error" in result:
        st.warning(result["error"])
        st.info("Run: `python -m utils.model_training --disease stroke` after adding `data/stroke.csv`.")
    else:
        st.markdown('<div class="section-title">📊 Analysis Output</div>', unsafe_allow_html=True)
        col_res, col_space = st.columns([1.5, 1])
        with col_res:
            result_card(result)

        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.subheader("📌 Important Risk Factors")
            factors = result.get("top_factors", [])
            if factors:
                for f in factors:
                    feat_name = f["feature"]
                    importance_pct = min(100.0, max(0.0, float(f["importance"]) * 100.0))
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 0.8rem; background-color: var(--secondary-background-color); padding: 0.8rem 1.2rem; border-radius: 12px; border: 1px solid var(--secondary-background-color);">
                            <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.3rem; color: var(--text-color);">
                                <span>{feat_name}</span>
                                <span>{f['importance']:.4f}</span>
                            </div>
                            <div style="background-color: rgba(0,0,0,0.1); border-radius: 6px; height: 8px; width: 100%;">
                                <div style="background: linear-gradient(90deg, #0ea5e9, #8b5cf6); height: 100%; border-radius: 6px; width: {importance_pct}%;"></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Feature importance is not available for this model.")

        with col2:
            st.subheader("📄 Download Clinical Report")
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

        st.markdown(
            """
            <div class="disclaimer-box">
                <p>⚠️ <strong>Medical Disclaimer:</strong> This prediction is generated by an ML model and is not a medical diagnosis. 
                Always consult a qualified healthcare professional for medical decisions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
