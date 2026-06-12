import streamlit as st
from pathlib import Path
from utils.css import inject_custom_css, render_sidebar

st.set_page_config(
    page_title="CareRisk AI | Healthcare Risk Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS and render unified sidebar
inject_custom_css()
render_sidebar()

# ==========================================
# Hero Section
# ==========================================
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">AI-Powered Disease Risk Screening</h1>
        <p class="hero-subtitle">
            Assess diabetes, heart disease, and stroke risk using ensemble machine learning classifiers with explainable AI (XAI) and downloadable clinical health reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Centered call to action buttons directly under the hero
col_btn1, col_btn2, _ = st.columns([1, 1, 2.5])
with col_btn1:
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    st.page_link("pages/1_Diabetes_Prediction.py", label="Start Diabetes Screening 🚀", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col_btn2:
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    st.page_link("pages/4_Model_Comparison.py", label="View Model Benchmarks 📊", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# Dashboard Core Metric Explanations
# ==========================================
st.markdown('<div class="section-title">📊 Platform Capabilities</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🧮</div>
        <h4>3 Modules</h4>
        <p>Screening pipelines for Diabetes, Heart Disease, and Stroke.</p>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🤖</div>
        <h4>11+ Models</h4>
        <p>Evaluates multiple algorithms to select the optimal predictor.</p>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🧠</div>
        <h4>Explainable AI</h4>
        <p>SHAP-based transparent feature contributions for results.</p>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">📄</div>
        <h4>PDF Reports</h4>
        <p>Color-coded reports ready for clinical review and download.</p>
    </div>""", unsafe_allow_html=True)

# ==========================================
# Disease Risk Screening Modules (Equal-Height Cards)
# ==========================================
st.markdown('<div class="section-title">🏥 Disease Risk Screening Modules</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)
with d1:
    st.markdown(
        """
        <div class="disease-card-wrapper">
            <div class="disease-card-body">
                <div class="disease-icon">🩸</div>
                <h3>Diabetes Screening</h3>
                <p>Assesses physiological markers like glucose levels, BMI, insulin, and age using trained ensemble ML models.</p>
                <div class="disease-tags">
                    <span class="disease-tag">Glucose</span>
                    <span class="disease-tag">BMI</span>
                    <span class="disease-tag">Age</span>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Diabetes_Prediction.py", label="Run Diabetes Analysis →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with d2:
    st.markdown(
        """
        <div class="disease-card-wrapper">
            <div class="disease-card-body">
                <div class="disease-icon">❤️</div>
                <h3>Heart Disease Risk</h3>
                <p>Analyzes cardiovascular parameters such as chest pain types, blood pressure, ECG indicators, and cholesterol.</p>
                <div class="disease-tags">
                    <span class="disease-tag">Cholesterol</span>
                    <span class="disease-tag">BP</span>
                    <span class="disease-tag">ECG</span>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Heart_Disease_Prediction.py", label="Run Heart Analysis →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with d3:
    st.markdown(
        """
        <div class="disease-card-wrapper">
            <div class="disease-card-body">
                <div class="disease-icon">🧠</div>
                <h3>Stroke Risk Profile</h3>
                <p>Screens neurological indicators based on demographics, hypertension, blood glucose history, and smoking status.</p>
                <div class="disease-tags">
                    <span class="disease-tag">Hypertension</span>
                    <span class="disease-tag">Smoking</span>
                    <span class="disease-tag">Glucose</span>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Stroke_Prediction.py", label="Run Stroke Analysis →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# Footer & Disclaimers
# ==========================================
st.markdown(
    """
    <div class="disclaimer-box">
        <p>⚠️ <strong>Important Medical Disclaimer:</strong> CareRisk AI is an educational ML demonstration project and is NOT a diagnostic tool. 
        It does not substitute for professional medical advice, diagnosis, or treatment. 
        Always consult a qualified primary care provider or medical specialist for healthcare decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        CareRisk AI • Clinical Risk Intelligence Demo • Built with Streamlit, scikit-learn, CatBoost, Plotly, and FPDF.
    </div>
    """,
    unsafe_allow_html=True,
)
