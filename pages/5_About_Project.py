import streamlit as st

st.set_page_config(page_title="About Project | CareRisk AI", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About CareRisk AI")

st.markdown(
    """
    **CareRisk AI** is a full-stack machine learning healthcare project built with Streamlit.
    It predicts risk for Diabetes, Heart Disease, and Stroke using real datasets and multiple ML models.

    The goal is to demonstrate an end-to-end ML workflow:

    - Dataset loading
    - Data cleaning
    - Categorical encoding
    - Numerical scaling
    - Model training
    - Ensemble learning
    - Model comparison
    - Prediction UI
    - Explainability
    - PDF report generation
    - Deployment readiness
    """
)

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("🧠 Machine Learning")
    st.markdown(
        """
        Models included:

        - Logistic Regression
        - Decision Tree
        - Random Forest
        - Bagging Classifier
        - AdaBoost Classifier
        - Gradient Boosting
        - XGBoost
        - LightGBM
        - CatBoost
        - Voting Classifier
        - Stacking Classifier
        """
    )

with c2:
    st.subheader("🛠️ Engineering")
    st.markdown(
        """
        Engineering features:

        - Modular Python files
        - Cached model loading
        - Graceful missing-file handling
        - Reusable prediction functions
        - Reusable preprocessing pipeline
        - Streamlit multipage app
        - Plotly charts
        - FPDF reports
        """
    )

st.divider()

st.subheader("📦 Training Command")
st.code("python -m utils.model_training --all", language="bash")

st.subheader("▶️ Run Command")
st.code("streamlit run app.py", language="bash")

st.error(
    "⚠️ Medical disclaimer: This app is not a medical device and does not provide medical advice. "
    "Use it only as an educational ML project."
)
