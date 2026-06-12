import streamlit as st
from pathlib import Path
from utils.css import inject_custom_css

st.set_page_config(
    page_title="CareRisk AI | Healthcare Risk Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"

inject_custom_css()

# ==========================================
# Sidebar Redesign
# ==========================================
with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown("<h3>CareRisk AI</h3>", unsafe_allow_html=True)
    st.caption("ML-powered health risk screening")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background-color:#eff6ff; padding:10px; border-radius:8px; border:1px solid #bfdbfe; margin-bottom:1rem;">
            <p style="color:#1e3a8a; font-size:0.8rem; margin:0; font-weight:600;">
            ℹ️ Educational Demo Only
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# Hero Section
# ==========================================
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">AI-Powered Disease Risk Screening</h1>
        <p class="hero-subtitle">
        Predict diabetes, heart disease, and stroke risk using ensemble machine learning with explainable AI and downloadable health reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional CTAs in the hero section could be placed here, but Streamlit buttons don't float inside HTML.
# Instead, we place them right under the hero section in a centered column.
col_btn1, col_btn2, _ = st.columns([1, 1, 3])
with col_btn1:
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    st.page_link("pages/1_Diabetes_Prediction.py", label="Start Screening 🚀", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col_btn2:
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    st.page_link("pages/4_Model_Comparison.py", label="View Model Performance 📊", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# Metric Cards
# ==========================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem;">🧮</div>
        <h3>3</h3>
        <p class="title">Risk Modules</p>
        <p class="desc">Independent screening pipelines for major diseases.</p>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem;">🤖</div>
        <h3>11+</h3>
        <p class="title">ML Algorithms</p>
        <p class="desc">Ensemble evaluation dynamically ranks models.</p>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem;">🧠</div>
        <h3>XAI</h3>
        <p class="title">AI Explanation</p>
        <p class="desc">SHAP-based transparent feature importance.</p>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:2rem;">📄</div>
        <h3>PDF</h3>
        <p class="title">Clinical Reports</p>
        <p class="desc">Downloadable risk summaries for doctors.</p>
    </div>""", unsafe_allow_html=True)

# ==========================================
# Disease Risk Screening Modules (Cards)
# ==========================================
st.markdown('<div class="section-title">🏥 Disease Risk Screening Modules</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)
with d1:
    st.markdown(
        """
        <div class="disease-card">
            <div style="font-size:2.5rem; margin-bottom:1rem;">🩸</div>
            <h3>Diabetes Screening</h3>
            <p>Evaluates physiological risk markers including glucose levels, insulin levels, age, and pregnancy data using trained estimators.</p>
            <div>
                <span class="disease-tag">Glucose</span>
                <span class="disease-tag">BMI</span>
                <span class="disease-tag">Age</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Diabetes_Prediction.py", label="Run Diabetes Analysis →", use_container_width=True)

with d2:
    st.markdown(
        """
        <div class="disease-card">
            <div style="font-size:2.5rem; margin-bottom:1rem;">❤️</div>
            <h3>Heart Disease Risk</h3>
            <p>Analyzes cardiovascular indicators such as chest pain types, cholesterol, resting blood pressure, and vessel status.</p>
            <div>
                <span class="disease-tag">BP</span>
                <span class="disease-tag">Cholesterol</span>
                <span class="disease-tag">ECG</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Heart_Disease_Prediction.py", label="Run Heart Analysis →", use_container_width=True)

with d3:
    st.markdown(
        """
        <div class="disease-card">
            <div style="font-size:2.5rem; margin-bottom:1rem;">🧠</div>
            <h3>Stroke Risk Profile</h3>
            <p>Assesses neurological risk based on demographic data, hypertension, BMI, glucose fluctuations, and smoking history.</p>
            <div>
                <span class="disease-tag">Hypertension</span>
                <span class="disease-tag">Smoking</span>
                <span class="disease-tag">BMI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Stroke_Prediction.py", label="Run Stroke Analysis →", use_container_width=True)


# ==========================================
# Footer & Disclaimers
# ==========================================
st.markdown(
    """
    <div class="disclaimer-box">
        <p>⚠️ <strong>Medical Disclaimer:</strong> CareRisk AI is an educational demonstration project and is NOT a diagnostic tool. 
        It does not substitute for professional medical advice, diagnosis, or treatment. 
        Always consult a qualified primary care provider or medical specialist for healthcare decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        CareRisk AI • Enterprise-Grade Demo • Built with Streamlit, scikit-learn, CatBoost, Plotly, and FPDF.
    </div>
    """,
    unsafe_allow_html=True,
)
