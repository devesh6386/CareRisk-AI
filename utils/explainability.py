"""Explainability helpers for CareRisk AI.

This module provides:
 - get_feature_importance()   : raw importance scores from any model type
 - get_top_risk_factors()     : returns top factors with HUMAN-READABLE explanations
 - format_risk_factors()      : formats factors list for display (kept for back-compat)

SHAP is used internally if available.  If it fails, the module falls back to
feature_importances_ / coef_ / zeros.

The user NEVER sees raw SHAP values or raw importance numbers — only readable
sentences like:
  "Glucose: 168 mg/dL — Your glucose value is above the healthy range..."
"""

from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Disease-specific thresholds and explanation templates
# ---------------------------------------------------------------------------

# Each entry: (feature_key, check_fn, explanation_template)
# check_fn receives the raw input_dict value for that feature.
# explanation_template is an f-string with {value} placeholder.

_DIABETES_RULES = [
    ("Glucose",
     lambda v: v > 140,
     lambda v: f"Glucose: {v:.0f} mg/dL — Your glucose value is above the common healthy range (≤140 mg/dL) and may increase diabetes risk."),
    ("Glucose",
     lambda v: 100 < v <= 140,
     lambda v: f"Glucose: {v:.0f} mg/dL — Your glucose is in the pre-diabetes range (100–140 mg/dL). Monitoring is advised."),
    ("BMI",
     lambda v: v > 30,
     lambda v: f"BMI: {v:.1f} — BMI above 30 is considered obese and is a significant risk factor for diabetes."),
    ("BMI",
     lambda v: 25 < v <= 30,
     lambda v: f"BMI: {v:.1f} — BMI between 25 and 30 indicates overweight, which can contribute to diabetes risk."),
    ("BloodPressure",
     lambda v: v > 80,
     lambda v: f"Blood Pressure: {v:.0f} mm Hg — Elevated diastolic blood pressure may contribute to metabolic risk."),
    ("Age",
     lambda v: v > 45,
     lambda v: f"Age: {v:.0f} years — Diabetes risk generally increases after age 45."),
    ("DiabetesPedigreeFunction",
     lambda v: v > 0.5,
     lambda v: f"Diabetes Pedigree Function: {v:.2f} — A higher score suggests possible family history of diabetes, which increases risk."),
    ("Insulin",
     lambda v: v > 200 or (0 < v < 16),
     lambda v: f"Insulin: {v:.0f} µU/mL — Your insulin level is outside the common healthy range, which may indicate metabolic issues."),
    ("Pregnancies",
     lambda v: v > 5,
     lambda v: f"Pregnancies: {int(v)} — Higher number of pregnancies is associated with increased gestational diabetes history."),
]

_HEART_RULES = [
    ("age",
     lambda v: v > 50,
     lambda v: f"Age: {v:.0f} years — Heart disease risk increases significantly after age 50."),
    ("trestbps",
     lambda v: v > 130,
     lambda v: f"Resting Blood Pressure: {v:.0f} mm Hg — High resting blood pressure (>130 mm Hg) is a major cardiovascular risk factor."),
    ("chol",
     lambda v: v > 240,
     lambda v: f"Cholesterol: {v:.0f} mg/dL — High cholesterol (>240 mg/dL) increases the risk of artery blockages."),
    ("thalach",
     lambda v: v < 120,
     lambda v: f"Max Heart Rate: {v:.0f} bpm — A lower maximum heart rate (<120 bpm) may indicate reduced cardiovascular fitness."),
    ("oldpeak",
     lambda v: v > 1.5,
     lambda v: f"ST Depression (oldpeak): {v:.1f} — A value above 1.5 suggests significant ST depression, a risk indicator for coronary artery disease."),
    ("ca",
     lambda v: v > 0,
     lambda v: f"Major Vessels: {int(v)} — Having {int(v)} major vessel(s) colored by fluoroscopy indicates possible blockage."),
    ("exang",
     lambda v: v == 1,
     lambda v: "Exercise-Induced Angina: Yes — Chest pain triggered by exercise strongly suggests coronary artery insufficiency."),
    ("cp",
     lambda v: v == 0,
     lambda v: "Chest Pain Type: Typical Angina — Typical angina chest pain is the most common heart disease symptom."),
    ("cp",
     lambda v: v == 3,
     lambda v: "Chest Pain Type: Asymptomatic — No chest pain (asymptomatic) can still be associated with high heart disease risk."),
    ("fbs",
     lambda v: v == 1,
     lambda v: "Fasting Blood Sugar: High (>120 mg/dL) — Elevated fasting blood sugar is associated with increased heart disease risk."),
]

_STROKE_RULES = [
    ("age",
     lambda v: v > 60,
     lambda v: f"Age: {v:.0f} years — Stroke risk increases significantly after age 60."),
    ("hypertension",
     lambda v: v == 1,
     lambda v: "Hypertension: Yes — High blood pressure is one of the strongest risk factors for stroke."),
    ("heart_disease",
     lambda v: v == 1,
     lambda v: "Heart Disease: Yes — A history of heart disease significantly increases the risk of stroke."),
    ("avg_glucose_level",
     lambda v: v > 140,
     lambda v: f"Average Glucose Level: {v:.1f} mg/dL — High glucose (>140 mg/dL) is linked to increased stroke risk, especially in diabetics."),
    ("avg_glucose_level",
     lambda v: 100 < v <= 140,
     lambda v: f"Average Glucose Level: {v:.1f} mg/dL — Your glucose is in the elevated range, which warrants monitoring."),
    ("bmi",
     lambda v: v > 30,
     lambda v: f"BMI: {v:.1f} — Obesity (BMI >30) is a recognized risk factor for stroke."),
    ("smoking_status",
     lambda v: str(v).lower() in ["smokes", "formerly smoked"],
     lambda v: f"Smoking Status: {v} — Smoking and former smoking are associated with significantly higher stroke risk."),
    ("age",
     lambda v: 45 < v <= 60,
     lambda v: f"Age: {v:.0f} years — Stroke risk starts increasing in middle age (45–60 years)."),
]

_RULES_MAP = {
    "diabetes": _DIABETES_RULES,
    "heart": _HEART_RULES,
    "stroke": _STROKE_RULES,
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _to_dense_array(data):
    """Convert sparse matrix/dataframe to dense numpy array."""
    if hasattr(data, "toarray"):
        return data.toarray()
    if isinstance(data, pd.DataFrame):
        return data.values
    return np.asarray(data)


def get_feature_importance(model: Any, feature_names: List[str]) -> pd.DataFrame:
    """Get feature importance from many model types.

    Priority:
    1. feature_importances_
    2. absolute Logistic Regression coefficients
    3. average importance from ensemble estimators
    4. zeros fallback
    """
    importances = None

    if hasattr(model, "feature_importances_"):
        importances = np.asarray(model.feature_importances_, dtype=float)
    elif hasattr(model, "coef_"):
        importances = np.abs(np.asarray(model.coef_)).ravel()
    elif hasattr(model, "estimators_"):
        collected = []
        for estimator in model.estimators_:
            # VotingClassifier stores tuples differently before/after fit.
            fitted_estimator = estimator
            if isinstance(estimator, tuple):
                fitted_estimator = estimator[1]
            if hasattr(fitted_estimator, "feature_importances_"):
                collected.append(np.asarray(fitted_estimator.feature_importances_, dtype=float))
            elif hasattr(fitted_estimator, "coef_"):
                collected.append(np.abs(np.asarray(fitted_estimator.coef_)).ravel())
        if collected:
            min_len = min(len(x) for x in collected)
            collected = [x[:min_len] for x in collected]
            importances = np.mean(collected, axis=0)

    if importances is None:
        importances = np.zeros(len(feature_names), dtype=float)

    # Align lengths safely.
    max_len = min(len(importances), len(feature_names))
    df = pd.DataFrame(
        {
            "feature": feature_names[:max_len],
            "importance": np.asarray(importances[:max_len], dtype=float),
        }
    )

    total = df["importance"].abs().sum()
    if total > 0:
        df["importance"] = df["importance"].abs() / total

    return df.sort_values("importance", ascending=False).reset_index(drop=True)


def _get_shap_ranking(input_data: Any, model: Any, feature_names: List[str], top_n: int) -> Optional[List[str]]:
    """Try SHAP to get ranked feature names. Returns None on any failure."""
    try:
        import shap
        dense_data = _to_dense_array(input_data)
        explainer = shap.Explainer(model, dense_data, feature_names=feature_names)
        shap_values = explainer(dense_data)
        values = shap_values.values

        # Binary classifiers may return shape (rows, features, classes).
        if values.ndim == 3:
            values = values[:, :, 1]

        importance = np.abs(values[0])
        max_len = min(len(importance), len(feature_names))
        result = pd.DataFrame(
            {
                "feature": feature_names[:max_len],
                "importance": importance[:max_len],
            }
        )
        result = result.sort_values("importance", ascending=False).head(top_n)
        if result["importance"].sum() == 0:
            return None
        return result["feature"].tolist()
    except Exception:
        return None


def _get_model_importance_ranking(model: Any, feature_names: List[str], top_n: int) -> List[str]:
    """Get ranked feature names using model feature importance."""
    df = get_feature_importance(model, feature_names).head(top_n)
    return df["feature"].tolist()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_top_risk_factors(
    input_data: Any,
    model: Any,
    feature_names: List[str],
    top_n: int = 5,
    disease_type: str = "",
    raw_input_dict: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Return top risk factors as human-readable explanations.

    Steps:
    1. Try SHAP to rank features by importance.
    2. Fall back to model feature_importances_ / coef_.
    3. For each top feature, look for a matching medical rule in raw_input_dict.
    4. If a rule fires, use its human-readable explanation.
    5. Otherwise, show the raw value with a neutral description.

    Returns a list of dicts:
      [{"feature": "Glucose", "importance": 0.34, "explanation": "Glucose: 168 mg/dL — ..."}, ...]
    """
    # Step 1+2: get ranked feature names
    ranked = _get_shap_ranking(input_data, model, feature_names, top_n)
    if ranked is None:
        ranked = _get_model_importance_ranking(model, feature_names, top_n)

    # Step 3+4+5: build human-readable explanations
    rules = _RULES_MAP.get(disease_type.lower().strip(), [])
    results = []

    for feat_name in ranked:
        explanation = None

        if raw_input_dict:
            # Match feature to original input key (handle OHE suffixes like "gender_Male")
            raw_key = _resolve_raw_key(feat_name, raw_input_dict)
            if raw_key is not None:
                raw_value = raw_input_dict[raw_key]
                # Check medical rules for this feature
                for rule_key, check_fn, explain_fn in rules:
                    if rule_key.lower() == raw_key.lower():
                        try:
                            if check_fn(raw_value):
                                explanation = explain_fn(raw_value)
                                break
                        except Exception:
                            continue

                # Fallback: generic readable message
                if explanation is None:
                    explanation = _generic_explanation(raw_key, raw_value, disease_type)

        if explanation is None:
            explanation = f"{feat_name} — This factor was identified as important by the model."

        results.append({
            "feature": feat_name,
            "importance": 1.0 / (len(ranked) + 1),  # placeholder importance; not shown
            "explanation": explanation,
        })

    return results


def format_risk_factors(
    top_factors: List[Dict[str, Any]],
    input_data: Dict[str, Any],
    disease_type: str,
) -> List[Dict[str, Any]]:
    """Kept for backwards compatibility. Returns factors as-is since explanations
    are now embedded directly by get_top_risk_factors()."""
    return top_factors


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resolve_raw_key(feat_name: str, raw_input_dict: Dict[str, Any]) -> Optional[str]:
    """Map a (possibly OHE-suffixed) feature name back to its raw input key.

    e.g. "gender_Male" -> "gender", "Glucose" -> "Glucose"
    """
    if feat_name in raw_input_dict:
        return feat_name
    # Try prefix match for OHE columns like "smoking_status_smokes"
    for key in raw_input_dict:
        if feat_name.lower().startswith(key.lower()):
            return key
    return None


def _generic_explanation(feature: str, value: Any, disease_type: str) -> str:
    """Generate a neutral readable explanation when no medical rule matches."""
    friendly_names = {
        "Pregnancies": "Pregnancies",
        "Glucose": "Glucose",
        "BloodPressure": "Blood Pressure",
        "SkinThickness": "Skin Thickness",
        "Insulin": "Insulin",
        "BMI": "BMI",
        "DiabetesPedigreeFunction": "Diabetes Pedigree Function",
        "Age": "Age",
        "age": "Age",
        "sex": "Sex",
        "cp": "Chest Pain Type",
        "trestbps": "Resting Blood Pressure",
        "chol": "Cholesterol",
        "fbs": "Fasting Blood Sugar",
        "restecg": "Resting ECG",
        "thalach": "Max Heart Rate",
        "exang": "Exercise-Induced Angina",
        "oldpeak": "ST Depression",
        "slope": "ST Slope",
        "ca": "Major Vessels",
        "thal": "Thalassemia",
        "gender": "Gender",
        "hypertension": "Hypertension",
        "heart_disease": "Heart Disease History",
        "ever_married": "Marital Status",
        "work_type": "Work Type",
        "Residence_type": "Residence Type",
        "avg_glucose_level": "Average Glucose Level",
        "bmi": "BMI",
        "smoking_status": "Smoking Status",
    }
    display_name = friendly_names.get(feature, feature)
    try:
        val_str = f"{float(value):.1f}" if isinstance(value, (int, float)) else str(value)
    except Exception:
        val_str = str(value)
    return f"{display_name}: {val_str} — This factor contributed to the model's risk assessment."
