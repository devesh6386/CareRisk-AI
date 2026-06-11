# 🩺 CareRisk AI

CareRisk AI is a professional, demo-ready Streamlit healthcare ML platform that predicts disease risk for:

1. 🩸 Diabetes
2. ❤️ Heart Disease
3. 🧠 Stroke

It is designed as a clean, professional, resume-worthy, and deployment-ready project for Streamlit Community Cloud.

> ⚠️ **Medical Disclaimer:** This project is for educational and portfolio purposes only. It is NOT medical advice, NOT a diagnosis tool, and must NOT replace consultation with a qualified doctor.

---

## 🚀 Features

- **Modern Streamlit multipage UI** with Inter font, glassmorphism cards, and micro-animations
- **Diabetes, Heart Disease, and Stroke** prediction pages
- **Real ML training pipeline** — 11 models compared per disease
- **Human-readable risk explanations** — no raw SHAP values shown to users
- **🤖 AI Assistant ("Ask CareRisk AI")** — Groq-powered follow-up Q&A after prediction
- **Professional PDF reports** with colour-coded risk level, readable factors, next steps
- **Model comparison dashboard** with Plotly charts
- **Graceful error handling** — no crashes if models, API key, or PDFs fail
- **Deployment-ready** for Streamlit Community Cloud

---

## 🤖 AI Assistant — Ask CareRisk AI

After each prediction, users can ask follow-up questions like:

- *"Why am I high risk?"*
- *"Which factors affected my result?"*
- *"How can I reduce my risk?"*
- *"Explain my result in simple words."*

The AI assistant uses **Groq** to provide short, friendly, plain-language explanations that:
- Never give a diagnosis
- Never prescribe medicines
- Always recommend consulting a doctor
- Always include a medical disclaimer

### Set up the AI assistant locally

1. Get your **Groq API key** from: https://console.groq.com/keys

2. Create the secrets file (copy the template):

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

3. Open `.streamlit/secrets.toml` and replace the placeholder:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. ⚠️ **Never push `secrets.toml` to GitHub!** It is already in `.gitignore` to prevent leaks.

### Set up on Streamlit Community Cloud

1. Open your app on **share.streamlit.io**
2. Go to **Settings → Secrets**
3. Add:

```toml
GROQ_API_KEY = "your_actual_groq_key_here"
```

4. Save and redeploy.

> If no API key is found, the AI assistant gracefully shows:
> *"AI assistant is unavailable. Please add GROQ_API_KEY in Streamlit secrets."*

---

## 🧠 ML Models Included

The training utility compares these models per disease:

| # | Model |
|---|-------|
| 1 | Logistic Regression |
| 2 | Decision Tree |
| 3 | Random Forest |
| 4 | Bagging Classifier |
| 5 | AdaBoost |
| 6 | Gradient Boosting |
| 7 | XGBoost |
| 8 | LightGBM |
| 9 | CatBoost |
| 10 | Voting Classifier |
| 11 | Stacking Classifier |

The best model is selected using **ROC-AUC** by default (falls back to F1-score).

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit, Vanilla CSS, Inter font |
| ML | scikit-learn, XGBoost, LightGBM, CatBoost |
| Explainability | SHAP + rule-based medical thresholds |
| AI Assistant | Groq (via `groq`) |
| Visualization | Plotly Express |
| PDF Reports | FPDF |
| Data | Pandas, NumPy |
| Serialization | Joblib |

---

## 📊 Datasets

Download these from Kaggle and place them in the `data/` folder:

| Disease | Kaggle Dataset | File Name |
|---|---|---|
| Diabetes | Pima Indians Diabetes Database | `data/diabetes.csv` |
| Heart Disease | Heart Disease Dataset by johnsmith88 | `data/heart.csv` |
| Stroke | Stroke Prediction Dataset by fedesoriano | `data/stroke.csv` |

---

## 📁 Folder Structure

```text
CareRisk-AI/
│
├── app.py                          # Main Streamlit homepage
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   ├── secrets.toml.example        # ✅ Safe to commit (template only)
│   └── secrets.toml                # ❌ NEVER commit (add to .gitignore)
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
│   ├── stroke_scaler.pkl
│   └── metrics.json
│
├── utils/
│   ├── preprocessing.py
│   ├── model_training.py
│   ├── prediction.py
│   ├── explainability.py           # Human-readable risk factors
│   ├── ai_assistant.py             # Gemini AI Q&A
│   ├── report_generator.py         # Professional PDF generation
│   └── css.py                      # Custom CSS injection
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
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add datasets

Download from Kaggle and place:

```text
data/diabetes.csv
data/heart.csv
data/stroke.csv
```

### 5. Train all models

```bash
python -m utils.model_training --all
```

### 6. (Optional) Set up AI Assistant

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Then add your Gemini API key inside secrets.toml
```

### 7. Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push the project to GitHub (model `.pkl` files must be committed).
2. Go to **share.streamlit.io** → New app → connect your repo.
3. Set main file: `app.py`
4. Under **Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Deploy. Done!

---

## 🔒 Security Notes

| File | Action |
|---|---|
| `.streamlit/secrets.toml` | ❌ Never commit — already in `.gitignore` |
| `.streamlit/secrets.toml.example` | ✅ Safe to commit — template only |
| `.env` | ❌ Never commit — already in `.gitignore` |

---

## 📄 PDF Reports

Each prediction generates a PDF containing:

- CareRisk AI branding header
- Disease type and timestamp
- Risk level (colour-coded)
- Model confidence percentage + visual bar
- Patient-entered health values
- Top risk factors (human-readable, no raw SHAP numbers)
- Suggested next steps
- Medical disclaimer

---

## 💼 Resume Bullets

- Built **CareRisk AI**, a full-stack Streamlit healthcare ML platform predicting diabetes, heart disease, and stroke risk using 11 ML models (XGBoost, LightGBM, CatBoost, Voting, Stacking).
- Implemented **Groq AI assistant** feature allowing users to ask plain-language follow-up questions about ML predictions.
- Engineered human-readable risk explanations using SHAP + medical threshold rules — eliminating confusing raw model scores from the user interface.
- Generated **professional PDF reports** with colour-coded results, risk factor summaries, and medical disclaimers.
- Deployed a **production-ready, crash-resilient** multipage Streamlit app on Streamlit Community Cloud with graceful error handling for missing models, API keys, and failures.

---

## ⚠️ Medical Disclaimer

CareRisk AI is **not a medical device**. It does not provide diagnosis, treatment, or medical advice. The predictions are generated using machine learning models trained on publicly available datasets and **may be inaccurate**. Risk scores are probabilistic estimates — not certainties. Always consult a qualified and licensed healthcare professional for medical decisions.
