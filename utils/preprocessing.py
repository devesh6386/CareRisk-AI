"""Preprocessing utilities for CareRisk AI.

This file keeps all dataset-specific information in one place.
The saved "scaler" files are actually full sklearn preprocessors:
- numerical imputation
- numerical scaling
- categorical imputation
- one-hot encoding
"""

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

DISEASE_CONFIG: Dict[str, Dict] = {
    "diabetes": {
        "display_name": "Diabetes",
        "data_path": DATA_DIR / "diabetes.csv",
        "target_candidates": ["Outcome", "outcome", "diabetes"],
        "features": [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age",
        ],
        "categorical_features": [],
        "numerical_features": [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age",
        ],
        "zero_as_missing": ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"],
        "model_path": MODEL_DIR / "diabetes_model.pkl",
        "scaler_path": MODEL_DIR / "diabetes_scaler.pkl",
    },
    "heart": {
        "display_name": "Heart Disease",
        "data_path": DATA_DIR / "heart.csv",
        "target_candidates": ["target", "Target", "condition", "HeartDisease", "heart_disease"],
        "features": [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
        ],
        "categorical_features": [],
        "numerical_features": [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
        ],
        "zero_as_missing": [],
        "model_path": MODEL_DIR / "heart_model.pkl",
        "scaler_path": MODEL_DIR / "heart_scaler.pkl",
    },
    "stroke": {
        "display_name": "Stroke",
        "data_path": DATA_DIR / "stroke.csv",
        "target_candidates": ["stroke", "Stroke"],
        "features": [
            "gender",
            "age",
            "hypertension",
            "heart_disease",
            "ever_married",
            "work_type",
            "Residence_type",
            "avg_glucose_level",
            "bmi",
            "smoking_status",
        ],
        "categorical_features": [
            "gender",
            "ever_married",
            "work_type",
            "Residence_type",
            "smoking_status",
        ],
        "numerical_features": [
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "bmi",
        ],
        "zero_as_missing": [],
        "model_path": MODEL_DIR / "stroke_model.pkl",
        "scaler_path": MODEL_DIR / "stroke_scaler.pkl",
    },
}


def get_config(disease: str) -> Dict:
    """Return configuration for one disease."""
    disease = disease.lower().strip()
    if disease not in DISEASE_CONFIG:
        raise ValueError(f"Unsupported disease: {disease}")
    return DISEASE_CONFIG[disease]


def find_target_column(df: pd.DataFrame, disease: str) -> str:
    """Find the target column from allowed names."""
    config = get_config(disease)
    for col in config["target_candidates"]:
        if col in df.columns:
            return col
    raise ValueError(
        f"Target column not found for {disease}. Expected one of: {config['target_candidates']}"
    )


def validate_required_columns(df: pd.DataFrame, disease: str) -> None:
    """Raise a helpful error if expected input columns are missing."""
    config = get_config(disease)
    missing = [col for col in config["features"] if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns for {config['display_name']}: {missing}. "
            f"Please check the CSV file and column names."
        )


def clean_dataframe(df: pd.DataFrame, disease: str) -> pd.DataFrame:
    """Clean dataset before training."""
    config = get_config(disease)
    df = df.copy()

    # Drop common index/id columns if they exist.
    for col in ["id", "Id", "ID", "Unnamed: 0"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    validate_required_columns(df, disease)

    # In Pima diabetes dataset, some medical measurements are stored as 0.
    # For these columns, 0 usually means missing measurement, not actual 0.
    for col in config.get("zero_as_missing", []):
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)

    # Ensure numerical columns are numeric.
    for col in config["numerical_features"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean categorical text.
    for col in config["categorical_features"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "N/A": np.nan})

    return df


def load_dataset(disease: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Load and split CSV into X and y."""
    config = get_config(disease)
    data_path = config["data_path"]

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path}. Download the Kaggle CSV and place it there."
        )

    df = pd.read_csv(data_path)
    df = clean_dataframe(df, disease)
    target_col = find_target_column(df, disease)

    X = df[config["features"]]
    y = df[target_col]

    # Convert target to 0/1 if needed.
    y = pd.to_numeric(y, errors="coerce")
    valid_rows = y.notna()
    X = X.loc[valid_rows].reset_index(drop=True)
    y = y.loc[valid_rows].astype(int).reset_index(drop=True)

    return X, y


def make_one_hot_encoder():
    """Create OneHotEncoder compatible with old/new scikit-learn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor(disease: str) -> ColumnTransformer:
    """Build preprocessing object for one disease."""
    config = get_config(disease)
    numerical_features = config["numerical_features"]
    categorical_features = config["categorical_features"]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_one_hot_encoder()),
        ]
    )

    transformers = []
    if numerical_features:
        transformers.append(("num", numeric_pipeline, numerical_features))
    if categorical_features:
        transformers.append(("cat", categorical_pipeline, categorical_features))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return preprocessor


def get_feature_names(preprocessor: ColumnTransformer, original_features: List[str]) -> List[str]:
    """Return transformed feature names after preprocessing."""
    try:
        names = preprocessor.get_feature_names_out()
        return [str(name).replace("num__", "").replace("cat__", "") for name in names]
    except Exception:
        return original_features


def make_input_dataframe(input_dict: Dict, disease: str) -> pd.DataFrame:
    """Convert Streamlit form values into dataframe with correct column order."""
    config = get_config(disease)
    row = {feature: input_dict.get(feature, np.nan) for feature in config["features"]}
    return pd.DataFrame([row], columns=config["features"])
