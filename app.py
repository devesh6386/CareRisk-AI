import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="CareRisk AI | Healthcare Risk Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"


from utils.css import inject_custom_css

inject_custom_css()

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.title("CareRisk AI")
    st.caption("ML-powered health risk screening")
    st.warning("This tool is for educational demo only, not medical advice.")

st.markdown(
    """
    <div class="hero-card">
        <h1>🩺 CareRisk AI</h1>
        <p>
        An enterprise-grade, clinical-grade predictive analytics platform designed to screen for
        Diabetes, Heart Disease, and Stroke using ensemble machine learning, explainable AI (SHAP),
        and dynamically generated medical reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Metric Cards
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""<div class="metric-card"><h3>3</h3><p>Risk Modules</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>11+</h3><p>Algorithms Compared</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>🤖 AI</h3><p>Ask CareRisk AI</p></div>""", unsafe_allow_html=True)
with m4:
    st.markdown("""<div class="metric-card"><h3>PDF</h3><p>Clinical Reports</p></div>""", unsafe_allow_html=True)

st.markdown('<div class="section-title">🏥 Disease Risk Screening Modules</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)
with d1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🩸 Diabetes Screening</h3>
            <p>Evaluates physiological risk markers including glucose levels, insulin levels, age, and pregnancy data using trained estimators.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with d2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>❤️ Heart Disease Risk</h3>
            <p>Analyzes cardiovascular indicators such as chest pain types, cholesterol, resting blood pressure, and vessel status.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with d3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 Stroke Risk Profile</h3>
            <p>Assesses neurological risk based on demographic data, hypertension, BMI, glucose fluctuations, and smoking history.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">⚙️ How it Works</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>1. Feed Data</h3>
            <p>Fill out the clinical parameters form on any risk screening page. Values map directly to verified clinical trial datasets.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>2. Run Inference</h3>
            <p>Our ensemble pipelines load serialized scalers and classifiers, producing instant probabilistic classification models.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>3. Download PDF</h3>
            <p>Generate a professional patient risk summary document featuring SHAP feature importance breakdowns instantly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">🛠️ Engineering Tech Stack</div>', unsafe_allow_html=True)

tech_col1, tech_col2 = st.columns([1.2, 1])
with tech_col1:
    st.markdown(
        """
        - **Machine Learning Pipeline**: Logistic Regression, Decision Tree, Random Forest, AdaBoost, Gradient Boosting, CatBoost, Stacking, and Voting.
        - **Preprocessing**: Robust scaling, categorical encoding, and serialization.
        - **Visualization**: Interactive Plotly Express graphs and SHAP-based feature importance plots.
        - **Reporting**: Programmatic document generation using `FPDF`.
        """
    )
with tech_col2:
    st.info(
        "💡 **Developer Note**:\n\n"
        "To initialize model files locally, run:\n"
        "`python -m utils.model_training --all`"
    )

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
        CareRisk AI • Portfolio Project • Built with Streamlit, scikit-learn, CatBoost, Plotly, and FPDF.
    </div>
    """,
    unsafe_allow_html=True,
)

