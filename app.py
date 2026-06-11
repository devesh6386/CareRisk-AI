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


def local_css():
    st.markdown(
        """
        <style>
        /* Responsive healthcare-style UI */
        .main-header {
            padding: 3rem 2.5rem;
            border-radius: 20px;
            background: linear-gradient(135deg, #0f766e 0%, #0369a1 100%);
            color: white;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 30px rgba(3, 105, 161, 0.2);
            text-align: center;
        }
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 0.8rem;
            color: #ffffff;
        }
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.95;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }
        
        /* Modern Metric Card */
        .metric-card {
            background-color: var(--background-color);
            border: 1px solid var(--secondary-background-color);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .metric-card h3 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            color: #0ea5e9;
        }
        .metric-card p {
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-color);
        }

        /* Modern Feature Card */
        .feature-card {
            background-color: var(--background-color);
            border: 1px solid var(--secondary-background-color);
            border-radius: 16px;
            padding: 1.8rem;
            height: 100%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
            border-color: #0ea5e9;
        }
        .feature-card h3 {
            margin-top: 0;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        .feature-card p {
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-color);
            opacity: 0.85;
            margin-bottom: 0;
        }

        /* Footer */
        .footer {
            margin-top: 4rem;
            padding: 2rem;
            border-top: 1px solid var(--secondary-background-color);
            text-align: center;
            font-size: 0.95rem;
            color: var(--text-color);
            opacity: 0.7;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                padding: 2rem 1.2rem;
                border-radius: 16px;
            }
            .main-header h1 {
                font-size: 2.2rem;
            }
            .main-header p {
                font-size: 1rem;
            }
            .metric-card {
                padding: 1rem;
            }
            .metric-card h3 {
                font-size: 1.8rem;
            }
            .feature-card {
                padding: 1.2rem;
            }
            .feature-card h3 {
                font-size: 1.1rem;
                flex-direction: column;
                text-align: center;
            }
            .feature-card p {
                text-align: center;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


local_css()

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.title("CareRisk AI")
    st.caption("ML-powered health risk screening")
    st.warning("This tool is for educational demo only, not medical advice.")

st.markdown(
    """
    <div class="main-header">
        <h1>🩺 CareRisk AI</h1>
        <p>
        A deployed-ready machine learning healthcare platform that predicts risk for
        Diabetes, Heart Disease, and Stroke using ensemble learning, explainability,
        and downloadable PDF reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="metric-card"><h3>3</h3><p>Disease Risk Modules</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card"><h3>11+</h3><p>ML Models Compared</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card"><h3>SHAP</h3><p>Explainability Fallback</p></div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card"><h3>PDF</h3><p>Report Download</p></div>""", unsafe_allow_html=True)

st.divider()

st.subheader("🚀 What this project includes")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 Real ML Pipeline</h3>
            <p>Training utility supports Logistic Regression, Decision Tree, Random Forest,
            Bagging, AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost,
            Voting, and Stacking classifiers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📊 Model Comparison</h3>
            <p>Compare Accuracy, Precision, Recall, F1-score, and ROC-AUC.
            The best model is selected automatically based on ROC-AUC or F1.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📄 Report Generator</h3>
            <p>Each prediction page can generate a clean downloadable PDF report
            with risk level, probability, inputs, and top risk factors.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

left, right = st.columns([1.2, 1])
with left:
    st.subheader("🧭 How to use")
    st.markdown(
        """
        1. Add the Kaggle CSV files inside the `data/` folder.
        2. Train models using `python -m utils.model_training --all`.
        3. Run the app using `streamlit run app.py`.
        4. Open the disease pages from the Streamlit sidebar.
        """
    )
with right:
    st.info(
        "If model files are missing, prediction pages will show: **Please train models first.**\n\n"
        "This keeps the deployed app safe from crashing."
    )

st.error(
    "⚠️ Medical disclaimer: CareRisk AI is not a diagnosis tool. It is an educational ML project. "
    "Always consult a qualified healthcare professional for medical decisions."
)

st.markdown(
    """
    <div class="footer">
        Built with Streamlit, scikit-learn, XGBoost, LightGBM, CatBoost, SHAP, Plotly, and FPDF.
    </div>
    """,
    unsafe_allow_html=True,
)
