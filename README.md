# 🩺 CareRisk AI

CareRisk AI is a complete Streamlit machine learning healthcare platform that predicts disease risk for:

1. Diabetes
2. Heart Disease
3. Stroke

It is designed as a clean, professional, resume-worthy, and deployment-ready project for Streamlit Community Cloud.

> ⚠️ Medical disclaimer: This project is for educational and portfolio purposes only. It is not medical advice, not a diagnosis tool, and must not replace consultation with a qualified doctor.

---

## 🚀 Features

- Modern Streamlit multipage UI
- Diabetes, Heart Disease, and Stroke prediction pages
- Real ML training pipeline
- Ensemble learning support
- Model comparison table
- Plotly model performance chart
- SHAP explainability with fallback feature importance
- PDF report generation using FPDF
- Graceful handling for missing datasets or missing models
- Deployment-ready GitHub structure

---

## 🧠 ML Models Included

The training utility compares the following models:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Bagging Classifier
- AdaBoost Classifier
- Gradient Boosting Classifier
- XGBoost Classifier
- LightGBM Classifier
- CatBoost Classifier
- Voting Classifier
- Stacking Classifier

The best model is selected using ROC-AUC by default. If ROC-AUC is unavailable, F1-score is used.

---

## 🧰 Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- LightGBM
- CatBoost
- SHAP
- Plotly
- Joblib
- FPDF

---

## 📊 Datasets

Download these datasets from Kaggle and place the CSV files inside the `data/` folder.

| Disease | Kaggle Dataset | Expected File Name |
|---|---|---|
| Diabetes | Pima Indians Diabetes Database | `data/diabetes.csv` |
| Heart Disease | Heart Disease Dataset by johnsmith88 | `data/heart.csv` |
| Stroke | Stroke Prediction Dataset by fedesoriano | `data/stroke.csv` |

Dataset links:

- Pima Indians Diabetes Database: `https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database`
- Heart Disease Dataset by johnsmith88: `https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset`
- Stroke Prediction Dataset by fedesoriano: `https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset`

### Expected target columns

| File | Target Column |
|---|---|
| `diabetes.csv` | `Outcome` |
| `heart.csv` | `target` |
| `stroke.csv` | `stroke` |

If your CSV has slightly different target names, edit `utils/preprocessing.py`.

---

## 📁 Folder Structure

```text
CareRisk-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── diabetes.csv
│   ├── heart.csv
│   └── stroke.csv
│
├── models/
│   ├── diabetes_model.pkl
│   ├── heart_model.pkl
│   ├── stroke_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── heart_scaler.pkl
│   └── stroke_scaler.pkl
│
├── utils/
│   ├── preprocessing.py
│   ├── model_training.py
│   ├── prediction.py
│   ├── explainability.py
│   └── report_generator.py
│
├── pages/
│   ├── 1_Diabetes_Prediction.py
│   ├── 2_Heart_Disease_Prediction.py
│   ├── 3_Stroke_Prediction.py
│   ├── 4_Model_Comparison.py
│   └── 5_About_Project.py
│
└── assets/
    └── logo.png
```

---

## ⚙️ How to Run Locally

### 1. Clone the project

```bash
git clone https://github.com/your-username/CareRisk-AI.git
cd CareRisk-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add datasets

Download the Kaggle CSV files and place them like this:

```text
data/diabetes.csv
data/heart.csv
data/stroke.csv
```

### 5. Train all models

```bash
python -m utils.model_training --all
```

This will create model files in the `models/` folder:

```text
models/diabetes_model.pkl
models/heart_model.pkl
models/stroke_model.pkl
models/diabetes_scaler.pkl
models/heart_scaler.pkl
models/stroke_scaler.pkl
models/metrics.json
```

### 6. Run Streamlit app

```bash
streamlit run app.py
```

---

## 🧪 Train One Disease Model Only

```bash
python -m utils.model_training --disease diabetes
python -m utils.model_training --disease heart
python -m utils.model_training --disease stroke
```

Choose model-selection metric:

```bash
python -m utils.model_training --disease diabetes --metric roc_auc
python -m utils.model_training --disease stroke --metric f1
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this project to GitHub.
2. Make sure `requirements.txt` is in the root folder.
3. Train models locally first.
4. Commit the generated `.pkl` model files inside the `models/` folder.
5. Go to Streamlit Community Cloud.
6. Create a new app from your GitHub repository.
7. Set main file path:

```text
app.py
```

8. Deploy.

If model files are missing, the app will not crash. It will show:

```text
Please train models first.
```

---

## 🧠 How Prediction Works

1. User enters clinical values in Streamlit form.
2. Input is converted to a Pandas DataFrame.
3. Saved preprocessor/scaler transforms the input.
4. Saved best model predicts disease risk.
5. Probability is converted into risk level:

| Probability | Risk Level |
|---|---|
| Below 40% | Low Risk |
| 40% to 70% | Medium Risk |
| Above 70% | High Risk |

---

## 📄 PDF Report

Each prediction page can generate a PDF report containing:

- Disease type
- Prediction result
- Risk probability
- Risk level
- Patient input values
- Important risk factors
- Medical disclaimer

---

## 💼 Resume Bullets

You can write this project on your resume like this:

- Built CareRisk AI, a Streamlit-based healthcare ML platform for diabetes, heart disease, and stroke risk prediction.
- Trained and compared 11 machine learning models including XGBoost, LightGBM, CatBoost, Voting, and Stacking classifiers.
- Implemented modular preprocessing, model training, model loading, prediction, explainability, and PDF report generation pipelines.
- Added SHAP-based explainability with fallback feature importance for model interpretability.
- Deployed a production-ready multipage Streamlit application with graceful error handling and downloadable patient risk reports.

---

## ⚠️ Medical Disclaimer

CareRisk AI is not a medical device. It does not provide diagnosis, treatment, or medical advice. The predictions are generated using machine learning models trained on public datasets and may be inaccurate. Always consult a qualified healthcare professional for medical decisions.
