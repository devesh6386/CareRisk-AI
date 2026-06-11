import streamlit as st
import pandas as pd

from utils.prediction import predict_heart
from utils.report_generator import generate_report
from utils.css import inject_custom_css

st.set_page_config(page_title="Heart Disease Prediction | CareRisk AI", page_icon="❤️", layout="wide")
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


st.markdown('<div class="section-title">❤️ Heart Disease Risk Screening</div>', unsafe_allow_html=True)
st.caption("Provide patient cardiovascular parameters to calculate risk probabilities.")

with st.form("heart_form"):
    st.markdown("##### 👤 Patient Diagnostics")
    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female (0)" if x == 0 else "Male (1)")
        cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3], help="0: Typical Angina, 1: Atypical Angina, 2: Non-anginal Pain, 3: Asymptomatic")
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=60, max_value=250, value=130)
        chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=80, max_value=700, value=240)

    with c2:
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], format_func=lambda x: "False (0)" if x == 0 else "True (1)")
        restecg = st.selectbox("Resting Electrocardiographic Results", options=[0, 1, 2], help="0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy")
        thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=250, value=150)
        exang = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "No (0)" if x == 0 else "Yes (1)")

    with c3:
        oldpeak = st.number_input("ST Depression Induced by Exercise (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        slope = st.selectbox("Slope of the Peak Exercise ST Segment", options=[0, 1, 2], help="0: Upsloping, 1: Flat, 2: Downsloping")
        ca = st.selectbox("Number of Major Vessels (0-4) Colored by Flourosopy", options=[0, 1, 2, 3, 4])
        thal = st.selectbox("Thalassemia (thal)", options=[0, 1, 2, 3], help="1: Normal, 2: Fixed Defect, 3: Reversable Defect")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Run Heart Disease Analysis", use_container_width=True)

if submitted:
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
    }

    result = predict_heart(input_data)

    if "error" in result:
        st.warning(result["error"])
        st.info("Run: `python -m utils.model_training --disease heart` after adding `data/heart.csv`.")
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

        st.markdown(
            """
            <div class="disclaimer-box">
                <p>⚠️ <strong>Medical Disclaimer:</strong> This prediction is generated by an ML model and is not a medical diagnosis. 
                Always consult a qualified healthcare professional for medical decisions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
