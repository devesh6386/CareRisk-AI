"""Explainability helpers for CareRisk AI."""

from typing import List, Dict, Any

import numpy as np
import pandas as pd


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

    # Keep lengths safe.
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


def get_top_risk_factors(
    input_data: Any,
    model: Any,
    feature_names: List[str],
    top_n: int = 5,
) -> List[Dict[str, float]]:
    """Try SHAP first, fallback to feature importance.

    Returns a list of dictionaries:
    [{"feature": "age", "importance": 0.23}, ...]
    """
    dense_data = _to_dense_array(input_data)

    # SHAP can fail for some model wrappers such as Voting/Stacking.
    try:
        import shap

        explainer = shap.Explainer(model, dense_data, feature_names=feature_names)
        shap_values = explainer(dense_data)
        values = shap_values.values

        # Binary classifiers may return shape: (rows, features, classes).
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

        if result["importance"].sum() > 0:
            result["importance"] = result["importance"] / result["importance"].sum()

        return result.to_dict(orient="records")
    except Exception:
        fallback = get_feature_importance(model, feature_names).head(top_n)
        return fallback.to_dict(orient="records")
