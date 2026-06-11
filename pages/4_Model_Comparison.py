import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Model Comparison | CareRisk AI", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE_DIR / "models" / "metrics.json"

st.title("📊 Model Comparison")
st.caption("Performance comparison for all trained ML models.")

if not METRICS_PATH.exists():
    st.warning("Model metrics not found. Please train models first.")
    st.code("python -m utils.model_training --all", language="bash")
    st.info("After training, this page will show Accuracy, Precision, Recall, F1-score, and ROC-AUC for every model.")
    st.stop()

with open(METRICS_PATH, "r", encoding="utf-8") as f:
    metrics_payload = json.load(f)

rows = []
for disease, records in metrics_payload.items():
    rows.extend(records)

if not rows:
    st.warning("No metrics available inside models/metrics.json.")
    st.stop()

metrics_df = pd.DataFrame(rows)

st.subheader("📋 Performance Table")
show_df = metrics_df.copy()
for col in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
    if col in show_df.columns:
        show_df[col] = pd.to_numeric(show_df[col], errors="coerce").round(4)

st.dataframe(show_df, use_container_width=True, hide_index=True)

success_df = metrics_df[metrics_df["status"] == "success"].copy()
if success_df.empty:
    st.error("No successful model training records found.")
    st.stop()

for col in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
    success_df[col] = pd.to_numeric(success_df[col], errors="coerce")

st.divider()

c1, c2 = st.columns([1, 1])
with c1:
    disease_filter = st.selectbox("Select disease", options=sorted(success_df["disease"].unique()))
with c2:
    metric_filter = st.selectbox("Select metric", options=["roc_auc", "f1", "accuracy", "precision", "recall"])

plot_df = success_df[success_df["disease"] == disease_filter].sort_values(metric_filter, ascending=False)

st.subheader(f"📈 {metric_filter.upper()} by Model - {disease_filter.title()}")
fig = px.bar(
    plot_df,
    x="model",
    y=metric_filter,
    text=metric_filter,
    title=f"{disease_filter.title()} Model Performance",
)
fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
fig.update_layout(xaxis_tickangle=-35, yaxis_range=[0, 1.05], height=520)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🏆 Best Models")

best_rows = []
for disease in sorted(success_df["disease"].unique()):
    temp = success_df[success_df["disease"] == disease].copy()
    metric = "roc_auc" if temp["roc_auc"].notna().any() else "f1"
    best = temp.sort_values(metric, ascending=False).iloc[0]
    best_rows.append(
        {
            "Disease": disease.title(),
            "Best Model": best["model"],
            "Selection Metric": metric,
            "Score": round(float(best[metric]), 4) if pd.notna(best[metric]) else None,
        }
    )

st.dataframe(pd.DataFrame(best_rows), use_container_width=True, hide_index=True)
