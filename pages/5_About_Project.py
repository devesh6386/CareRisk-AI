import streamlit as st
from utils.css import inject_custom_css, render_sidebar

st.set_page_config(
    page_title="About Project | CareRisk AI",
    page_icon="ℹ️",
    layout="wide",
)

# Inject custom CSS and render unified sidebar
inject_custom_css()
render_sidebar()

st.markdown('<div class="section-title">ℹ️ About CareRisk AI</div>', unsafe_allow_html=True)
st.caption("Detailed portfolio documentation of the CareRisk AI clinical screening platform.")

col_left, col_right = st.columns(2)

with col_left:
    # Problem Statement Card
    st.markdown(
        """
        <div class="about-card">
            <h3>🎯 Problem Statement</h3>
            <p>
                Early risk detection is one of the most critical challenges in modern healthcare. Diseases such as <strong>Diabetes</strong>, <strong>Heart Disease</strong>, and <strong>Stroke</strong> often develop silently, showing severe symptoms only when complications arise. Identifying high-risk individuals early allows clinicians and patients to take preventive action, saving lives and reducing medical costs.
            </p>
            <p>
                <strong>CareRisk AI</strong> addresses this problem by demonstrating a production-grade machine learning system that ingests patient physiological parameters, evaluates risk profiles using clinical estimators, and explains individual predictions using SHAP (SHapley Additive exPlanations) values.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Machine Learning Pipeline Card
    st.markdown(
        """
        <div class="about-card">
            <h3>⚙️ The Machine Learning Pipeline</h3>
            <ol>
                <li><strong>Data Preprocessing & Encoding</strong>: Drops identifiers, handles missing values (e.g. BMI/Glucose gaps), and encodes categorical inputs.</li>
                <li><strong>Robust Numerical Scaling</strong>: Implements <code>RobustScaler</code> / <code>StandardScaler</code> to normalize feature dimensions, ensuring stable boundaries.</li>
                <li><strong>Ensemble Benchmarking</strong>: Trains multiple estimators and chooses the optimal model using validation <strong>ROC-AUC</strong> or <strong>F1-score</strong>.</li>
                <li><strong>Serialization</strong>: Saves classifiers and preprocessors dynamically.</li>
                <li><strong>SHAP Fallback</strong>: Evaluates model gradients or tree partitions to calculate local risk contribution scores.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Deployment Card
    st.markdown(
        """
        <div class="about-card">
            <h3>🚀 Deployment & Operations</h3>
            <ul>
                <li><strong>Cloud Deployment</strong>: Deployed ready on <strong>Streamlit Community Cloud</strong> or containerized using <strong>Docker</strong>.</li>
                <li><strong>Decoupled Pipelines</strong>: Modular engineering allows pipeline training to run headlessly on staging/CI servers while the Streamlit runtime serves inference.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    # Core Features Card
    st.markdown(
        """
        <div class="about-card">
            <h3>⭐ Core Capabilities</h3>
            <ul>
                <li><strong>Multi-Module Risk Screening</strong>: Independent pipelines for Diabetes, Heart Disease, and Stroke.</li>
                <li><strong>Ensemble Decisioning</strong>: Automatically benchmarks 11+ classifiers (Gradient Boosting, CatBoost, Stacking) to execute predictions with the optimal model.</li>
                <li><strong>Clinician Actionable Reports</strong>: Generates formal clinical PDF summaries containing prediction details and top risk attributes.</li>
                <li><strong>Explainable AI (XAI)</strong>: Outlines SHAP-based feature importance contribution scores for every prediction.</li>
                <li><strong>Fail-Safe Inference</strong>: Automatically detects if trained model weights are missing and prompts local training.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Models & Tech Stack Card
    st.markdown(
        """
        <div class="about-card">
            <h3>🧠 Models & Engineering Stack</h3>
            <p><strong>Algorithms Benchmarked:</strong></p>
            <ul>
                <li>Linear & Trees: Logistic Regression, Decision Tree</li>
                <li>Bagging & Boosting: Random Forest, Bagging, AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost</li>
                <li>Ensemble Methods: Stacking Classifier, Voting Classifier</li>
            </ul>
            <p><strong>Engineering Tech Stack:</strong></p>
            <ul>
                <li>Backend/Inference: Python, Streamlit Multipage</li>
                <li>Machine Learning: scikit-learn, CatBoost, XGBoost, LightGBM, SHAP</li>
                <li>Data/Visualization: Pandas, NumPy, Plotly Express</li>
                <li>Document Generation: FPDF (Programmatic PDF building)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dataset Reference Card
    st.markdown(
        """
        <div class="about-card">
            <h3>📊 Dataset Reference Information</h3>
            <p>The models are trained on established, anonymous clinical reference datasets:</p>
            <ul>
                <li><strong>Diabetes</strong>: <em>Pima Indians Diabetes Database</em> (NHGRI). Includes variables like Glucose, Insulin, BMI, Age, and Genetics.</li>
                <li><strong>Heart Disease</strong>: <em>Cleveland & Johnsmith88 Heart Disease Dataset</em>. Measures chest pain indicators, resting BP, cholesterol, ECG, and vessel status.</li>
                <li><strong>Stroke</strong>: <em>Fedesoriano Stroke Prediction Dataset</em>. Captures demographics, hypertension history, smoking indicators, and glucose fluctuations.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Disclaimer Box
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
