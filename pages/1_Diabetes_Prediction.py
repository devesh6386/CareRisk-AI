import streamlit as st
import pandas as pd

from utils.prediction import predict_diabetes
from utils.report_generator import generate_report
from utils.css import inject_custom_css

st.set_page_config(page_title="Diabetes Prediction | CareRisk AI", page_icon="🩸", layout="wide")
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


st.markdown('<div class="section-title">🩸 Diabetes Risk Screening</div>', unsafe_allow_html=True)
st.caption("Provide patient physiological data to generate risk probabilities.")

with st.form("diabetes_form"):
    st.markdown("##### 👤 Patient Diagnostics")
    c1, c2 = st.columns(2)
    with c1:
        Pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, help="Number of times pregnant")
        Glucose = st.number_input("Glucose Concentration", min_value=0.0, max_value=300.0, value=120.0, help="2-hour oral glucose tolerance test")
        BloodPressure = st.number_input("Diastolic Blood Pressure (mm Hg)", min_value=0.0, max_value=200.0, value=70.0)
        SkinThickness = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0)
    with c2:
        Insulin = st.number_input("2-Hour Serum Insulin (mu U/ml)", min_value=0.0, max_value=900.0, value=80.0)
        BMI = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=80.0, value=28.0)
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.45, help="Genetic family history score")
        Age = st.number_input("Age (years)", min_value=1, max_value=120, value=35)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Run Diabetes Risk Analysis", use_container_width=True)

if submitted:
    input_data = {
        "Pregnancies": Pregnancies,
        "Glucose": Glucose,
        "BloodPressure": BloodPressure,
        "SkinThickness": SkinThickness,
        "Insulin": Insulin,
        "BMI": BMI,
        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
        "Age": Age,
    }

    result = predict_diabetes(input_data)

    if "error" in result:
        st.warning(result["error"])
        st.info("Run: `python -m utils.model_training --disease diabetes` after adding `data/diabetes.csv`.")
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

        st.markdown(
            """
            <div class="disclaimer-box">
                <p>⚠️ <strong>Medical Disclaimer:</strong> This prediction is generated by an ML model and is not a medical diagnosis. 
                Always consult a qualified healthcare professional for medical decisions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
