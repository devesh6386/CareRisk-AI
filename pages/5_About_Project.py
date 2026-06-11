import streamlit as st
from utils.css import inject_custom_css

st.set_page_config(page_title="About Project | CareRisk AI", page_icon="ℹ️", layout="wide")
inject_custom_css()

st.markdown('<div class="section-title">ℹ️ About CareRisk AI</div>', unsafe_allow_html=True)
st.caption("Detailed portfolio documentation of the CareRisk AI clinical screening platform.")

# Problem Statement & Objective
st.markdown("### 🎯 Problem Statement")
st.markdown(
    """
    Early risk detection is one of the most critical challenges in modern healthcare. Diseases such as **Diabetes**, **Heart Disease**, and **Stroke** 
    often develop silently, showing severe symptoms only when complications arise. Identifying high-risk individuals early 
    allows clinicians and patients to take preventive action, saving lives and reducing medical costs.
    
    **CareRisk AI** addresses this problem by demonstrating a production-grade machine learning system that ingests patient physiological parameters, 
    evaluates risk profile using clinical estimators, and explains individual predictions using SHAP (SHapley Additive exPlanations) values.
    """
)

st.divider()

# Features & Capabilities
st.markdown("### ⭐ Core Features")
col_feat1, col_feat2 = st.columns(2)
with col_feat1:
    st.markdown(
        """
        - **Multi-Module Risk Screening**: Independent pipelines for Diabetes, Heart Disease, and Stroke.
        - **Ensemble Decisioning**: Automatically benchmarks 11+ classifiers (Gradient Boosting, CatBoost, Stacking) to execute prediction with the optimal model.
        - **Clinician Actionable Reports**: Generates formal clinical PDF summaries containing prediction details and top risk attributes.
        """
    )
with col_feat2:
    st.markdown(
        """
        - **Explainable AI (XAI)**: Outlines SHAP-based feature importance contribution scores for every prediction.
        - **Modern Dark-Mode Adaptive UI**: Custom CSS stylesheet guarantees high-contrast readability in both light and dark settings.
        - **Fail-Safe Inference**: Automatically detects if trained model weights are missing and prompts local training.
        """
    )

st.divider()

# Machine Learning Pipeline
st.markdown("### ⚙️ The Machine Learning Pipeline")
st.markdown(
    """
    ```mermaid
    graph LR
        A[Kaggle CSV Data] --> B[Data Cleaning & Encoding]
        B --> C[Robust Numerical Scaling]
        C --> D[11+ Estimator Benchmarking]
        D --> E[Optimal Model Serialization (.pkl)]
        E --> F[Inference Engine (Streamlit)]
        F --> G[Explainability & PDF Reports]
    ```
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    1. **Data Preprocessing & Encoding**: Drops identifiers, handles missing values (e.g., BMI/Glucose gaps), and encodes categorical inputs.
    2. **Scaling**: Implements `RobustScaler` / `StandardScaler` to normalize feature dimensions, ensuring stable boundaries.
    3. **Ensemble Benchmarking**: Trains multiple estimators and chooses the optimal model using validation **ROC-AUC** or **F1-score**.
    4. **Serialization**: Saves classifiers and preprocessors dynamically.
    5. **SHAP Fallback**: Evaluates model gradients or tree partitions to calculate local risk contribution scores.
    """
)

st.divider()

# Models & Technology Stack
st.markdown("### 🧠 Models Benchmarked")
st.markdown(
    """
    - **Linear & Trees**: Logistic Regression, Decision Tree
    - **Bagging & Boosting**: Random Forest, Bagging Classifier, AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost
    - **Ensemble Methods**: Stacking Classifier, Voting Classifier
    """
)

st.markdown("### 🛠️ Engineering Tech Stack")
st.markdown(
    """
    - **Backend/Inference**: Python, Streamlit Multipage
    - **Machine Learning**: scikit-learn, CatBoost, XGBoost, LightGBM, SHAP
    - **Data/Visualization**: Pandas, NumPy, Plotly Express, Mermaid.js
    - **Document Generation**: FPDF (Programmatic PDF building)
    """
)

st.divider()

# Dataset Information
st.markdown("### 📊 Dataset Reference Information")
st.markdown(
    """
    The models are trained on established, anonymous clinical reference datasets:
    - **Diabetes**: *Pima Indians Diabetes Database* (NHGRI). Includes variables like Glucose, Insulin, BMI, Age, and Genetics.
    - **Heart Disease**: *Cleveland & Johnsmith88 Heart Disease Dataset*. Measures chest pain indicators, resting BP, cholesterol, ECG, and vessel status.
    - **Stroke**: *Fedesoriano Stroke Prediction Dataset*. Captures demographics, hypertension history, smoking indicators, and glucose fluctuations.
    """
)

# Deployment Details
st.markdown("### 🚀 Deployment Details")
st.markdown(
    """
    - Deployed ready on **Streamlit Community Cloud** or containerized using **Docker**.
    - Fully modular pipeline: training can be executed headlessly on staging servers, while the Streamlit runtime serves inference.
    """
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
