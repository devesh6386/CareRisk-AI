"""Training script for CareRisk AI.

Usage:
    python -m utils.model_training --all
    python -m utils.model_training --disease diabetes
    python -m utils.model_training --disease heart --metric roc_auc
    python -m utils.model_training --disease stroke --metric f1
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from utils.preprocessing import (
    MODEL_DIR,
    DISEASE_CONFIG,
    build_preprocessor,
    get_config,
    get_feature_names,
    load_dataset,
)

try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None

try:
    from lightgbm import LGBMClassifier
except Exception:
    LGBMClassifier = None

try:
    from catboost import CatBoostClassifier
except Exception:
    CatBoostClassifier = None


RANDOM_STATE = 42


def make_bagging_classifier() -> BaggingClassifier:
    """Create BaggingClassifier compatible with multiple sklearn versions."""
    tree = DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE)
    try:
        return BaggingClassifier(
            estimator=tree,
            n_estimators=80,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
    except TypeError:
        return BaggingClassifier(
            base_estimator=tree,
            n_estimators=80,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )


def get_models() -> Dict[str, Any]:
    """Return all models used in this project."""
    models: Dict[str, Any] = {
        "LogisticRegression": LogisticRegression(
            max_iter=1500,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "DecisionTreeClassifier": DecisionTreeClassifier(
            max_depth=7,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "RandomForestClassifier": RandomForestClassifier(
            n_estimators=160,
            max_depth=None,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "BaggingClassifier": make_bagging_classifier(),
        "AdaBoostClassifier": AdaBoostClassifier(
            n_estimators=120,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
        ),
        "GradientBoostingClassifier": GradientBoostingClassifier(
            n_estimators=140,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
        ),
    }

    if XGBClassifier is not None:
        models["XGBClassifier"] = XGBClassifier(
            n_estimators=160,
            learning_rate=0.05,
            max_depth=3,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    if LGBMClassifier is not None:
        models["LGBMClassifier"] = LGBMClassifier(
            n_estimators=160,
            learning_rate=0.05,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            verbose=-1,
        )

    if CatBoostClassifier is not None:
        models["CatBoostClassifier"] = CatBoostClassifier(
            iterations=160,
            learning_rate=0.05,
            depth=4,
            loss_function="Logloss",
            eval_metric="AUC",
            auto_class_weights="Balanced",
            random_state=RANDOM_STATE,
            verbose=0,
        )

    # Voting and stacking use strong but not too heavy base learners.
    voting_estimators = [
        ("lr", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE)),
        ("rf", RandomForestClassifier(n_estimators=120, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1)),
        ("gb", GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, random_state=RANDOM_STATE)),
    ]
    if XGBClassifier is not None:
        voting_estimators.append(
            (
                "xgb",
                XGBClassifier(
                    n_estimators=100,
                    learning_rate=0.05,
                    max_depth=3,
                    eval_metric="logloss",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            )
        )

    models["VotingClassifier"] = VotingClassifier(
        estimators=voting_estimators,
        voting="soft",
        n_jobs=-1,
    )

    models["StackingClassifier"] = StackingClassifier(
        estimators=voting_estimators,
        final_estimator=LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE),
        stack_method="predict_proba",
        n_jobs=-1,
    )

    return models


def evaluate_model(model, X_test, y_test) -> Dict[str, float]:
    """Calculate model metrics."""
    y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        scores = model.decision_function(X_test)
        y_prob = 1 / (1 + np.exp(-scores))
    else:
        y_prob = y_pred

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": np.nan,
    }

    try:
        if len(np.unique(y_test)) == 2:
            metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
    except Exception:
        metrics["roc_auc"] = np.nan

    return {key: float(value) if not pd.isna(value) else None for key, value in metrics.items()}


def train_and_compare(disease: str, metric: str = "roc_auc") -> Tuple[Any, Any, pd.DataFrame]:
    """Train all models, compare metrics, save best model and preprocessor."""
    config = get_config(disease)
    MODEL_DIR.mkdir(exist_ok=True)

    X, y = load_dataset(disease)

    stratify = y if y.nunique() == 2 and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )

    preprocessor = build_preprocessor(disease)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    if hasattr(X_train_processed, "toarray"):
        X_train_processed = X_train_processed.toarray()
    if hasattr(X_test_processed, "toarray"):
        X_test_processed = X_test_processed.toarray()

    feature_names = get_feature_names(preprocessor, config["features"])
    X_train_processed = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_processed = pd.DataFrame(X_test_processed, columns=feature_names)

    rows = []
    fitted_models: Dict[str, Any] = {}

    for name, model in get_models().items():
        print(f"Training {disease}: {name}")
        try:
            model.fit(X_train_processed, y_train)
            model_metrics = evaluate_model(model, X_test_processed, y_test)
            fitted_models[name] = model
            rows.append({"disease": disease, "model": name, **model_metrics, "status": "success"})
        except Exception as exc:
            rows.append(
                {
                    "disease": disease,
                    "model": name,
                    "accuracy": None,
                    "precision": None,
                    "recall": None,
                    "f1": None,
                    "roc_auc": None,
                    "status": f"failed: {exc}",
                }
            )

    results_df = pd.DataFrame(rows)

    success_df = results_df[results_df["status"] == "success"].copy()
    if success_df.empty:
        raise RuntimeError(f"No model trained successfully for {disease}.")

    if metric not in ["roc_auc", "f1", "accuracy", "precision", "recall"]:
        metric = "roc_auc"

    # If selected metric is missing, use f1.
    if success_df[metric].isna().all():
        metric = "f1"

    success_df["selection_metric"] = success_df[metric].fillna(-1)
    best_row = success_df.sort_values("selection_metric", ascending=False).iloc[0]
    best_model_name = best_row["model"]
    best_model = fitted_models[best_model_name]

    joblib.dump(best_model, config["model_path"])
    joblib.dump(preprocessor, config["scaler_path"])

    print(f"Best {disease} model: {best_model_name} by {metric} = {best_row[metric]}")
    return best_model, preprocessor, results_df


def save_metrics(all_metrics: Dict[str, pd.DataFrame]) -> None:
    """Save combined metrics to models/metrics.json."""
    MODEL_DIR.mkdir(exist_ok=True)
    payload = {}
    for disease, df in all_metrics.items():
        payload[disease] = df.to_dict(orient="records")

    metrics_path = MODEL_DIR / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved metrics to {metrics_path}")


def main():
    parser = argparse.ArgumentParser(description="Train CareRisk AI models")
    parser.add_argument("--all", action="store_true", help="Train all disease models")
    parser.add_argument(
        "--disease",
        choices=list(DISEASE_CONFIG.keys()),
        help="Train one disease model",
    )
    parser.add_argument(
        "--metric",
        default="roc_auc",
        choices=["roc_auc", "f1", "accuracy", "precision", "recall"],
        help="Metric used to select best model",
    )
    args = parser.parse_args()

    if not args.all and not args.disease:
        parser.error("Use --all or --disease diabetes|heart|stroke")

    diseases = list(DISEASE_CONFIG.keys()) if args.all else [args.disease]
    all_metrics = {}

    for disease in diseases:
        try:
            _, _, metrics_df = train_and_compare(disease, metric=args.metric)
            all_metrics[disease] = metrics_df
        except Exception as exc:
            print(f"Training failed for {disease}: {exc}")
            all_metrics[disease] = pd.DataFrame(
                [
                    {
                        "disease": disease,
                        "model": "N/A",
                        "accuracy": None,
                        "precision": None,
                        "recall": None,
                        "f1": None,
                        "roc_auc": None,
                        "status": f"failed: {exc}",
                    }
                ]
            )

    save_metrics(all_metrics)


if __name__ == "__main__":
    main()
