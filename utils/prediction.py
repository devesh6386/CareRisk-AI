"""Prediction utilities for CareRisk AI."""

from pathlib import Path
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.preprocessing import get_config, make_input_dataframe, get_feature_names
from utils.explainability import get_top_risk_factors

BASE_DIR = Path(__file__).resolve().parents[1]


@st.cache_resource(show_spinner=False)
def load_model_bundle(disease: str):
    """Load model and preprocessor from disk.

    The saved scaler file is a complete sklearn ColumnTransformer preprocessor.
    Returns (model, preprocessor, error_message_or_None).
    """
    config = get_config(disease)
    model_path = config["model_path"]
    scaler_path = config["scaler_path"]

    if not model_path.exists() or not scaler_path.exists():
        return None, None, f"Please train models first. Missing: {model_path.name} or {scaler_path.name}"

    try:
        model = joblib.load(model_path)
        preprocessor = joblib.load(scaler_path)
        return model, preprocessor, None
    except Exception as exc:
        return None, None, f"Could not load model files: {exc}"


def probability_to_risk(probability: float) -> str:
    """Convert probability into a user-friendly risk label."""
    if probability < 0.40:
        return "Low Risk"
    if probability <= 0.70:
        return "Medium Risk"
    return "High Risk"


def risk_color(risk_level: str) -> str:
    """Return a display color hex string for the given risk level."""
    colors = {
        "Low Risk": "#16a34a",
        "Medium Risk": "#f59e0b",
        "High Risk": "#dc2626",
    }
    return colors.get(risk_level, "#64748b")


def _predict_probability(model, X_processed) -> float:
    """Safely calculate positive-class probability from any sklearn-compatible model."""
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_processed)
        if proba.shape[1] == 1:
            return float(proba[0][0])
        return float(proba[0][1])

    if hasattr(model, "decision_function"):
        score = model.decision_function(X_processed)[0]
        return float(1 / (1 + np.exp(-score)))

    prediction = model.predict(X_processed)[0]
    return float(prediction)


def predict_disease(input_dict: Dict[str, Any], disease: str) -> Dict[str, Any]:
    """Core prediction function used by all disease pages.

    Returns a result dict containing:
      - prediction        : int (0 or 1)
      - probability       : float (0-1)
      - probability_percent: float
      - risk_level        : str
      - risk_color        : str
      - model_used        : str (technical, hidden from main UI)
      - top_factors       : list of dicts with human-readable 'explanation' field
      - input_df          : raw DataFrame (used internally by report generator)
    """
    model, preprocessor, error = load_model_bundle(disease)
    config = get_config(disease)

    if error:
        return {"error": error}

    try:
        input_df = make_input_dataframe(input_dict, disease)
        transformed = preprocessor.transform(input_df)

        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()

        feature_names = get_feature_names(preprocessor, config["features"])
        X_processed = pd.DataFrame(transformed, columns=feature_names)

        probability = _predict_probability(model, X_processed)
        prediction = int(probability >= 0.5)
        level = probability_to_risk(probability)

        # Pass raw input_dict so explainability can generate human-readable text
        top_factors = get_top_risk_factors(
            input_data=X_processed,
            model=model,
            feature_names=feature_names,
            top_n=5,
            disease_type=disease,
            raw_input_dict=input_dict,
        )

        return {
            "prediction": prediction,
            "probability": probability,
            "probability_percent": round(probability * 100, 2),
            "risk_level": level,
            "risk_color": risk_color(level),
            "model_used": model.__class__.__name__,
            "top_factors": top_factors,
            "input_df": input_df,
        }
    except Exception as exc:
        return {"error": f"Prediction failed: {exc}"}


def predict_diabetes(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    return predict_disease(input_dict, "diabetes")


def predict_heart(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    return predict_disease(input_dict, "heart")


def predict_stroke(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    return predict_disease(input_dict, "stroke")
