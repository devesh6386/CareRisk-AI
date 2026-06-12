import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.css import inject_custom_css, render_sidebar

st.set_page_config(
    page_title="Model Comparison | CareRisk AI",
    page_icon="📊",
    layout="wide",
)

# Inject custom CSS and render unified sidebar
inject_custom_css()
render_sidebar()

BASE_DIR = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE_DIR / "models" / "metrics.json"

st.markdown('<div class="section-title">📊 Model Comparison Dashboard</div>', unsafe_allow_html=True)
st.caption("Performance benchmarking for all trained machine learning pipelines.")

if not METRICS_PATH.exists():
    st.markdown(
        """
        <div class="disclaimer-box" style="background-color: rgba(239, 68, 68, 0.04) !important; border-color: rgba(239, 68, 68, 0.15) !important;">
            <p><strong>ℹ️ Benchmark Metrics Not Found</strong></p>
            <p>To populate this page with performance graphs, please execute the pipeline training command inside your terminal:
            <br><code>python -m utils.model_training --all</code></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# Metric Descriptions Section
st.markdown('<div class="section-title">💡 Understanding Healthcare ML Metrics</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown("""
        <div class="metric-card">
            <h4>🎯 Accuracy</h4>
            <p>Percentage of correctly classified patients. Good overall measure but can be misleading on imbalanced datasets.</p>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div class="metric-card">
            <h4>🔬 Precision</h4>
            <p>Of all predicted high-risk patients, how many were actually high-risk. Minimizes False Positives.</p>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
        <div class="metric-card">
            <h4>📢 Recall (Sensitivity)</h4>
            <p>Percentage of actual high-risk patients correctly identified. Crucial in clinical setups to avoid missing patients.</p>
        </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
        <div class="metric-card">
            <h4>⚖️ F1-Score</h4>
            <p>Harmonic mean of Precision and Recall. Essential metric when seeking a balanced clinical classifier.</p>
        </div>
    """, unsafe_allow_html=True)
with c5:
    st.markdown("""
        <div class="metric-card">
            <h4>📈 ROC-AUC</h4>
            <p>Area Under the ROC Curve. Measures how well the model distinguishes between risk levels across all probability thresholds.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load metrics data
with open(METRICS_PATH, "r", encoding="utf-8") as f:
    metrics_payload = json.load(f)

rows = []
for disease, records in metrics_payload.items():
    rows.extend(records)

if not rows:
    st.warning("No metrics available inside models/metrics.json.")
    st.stop()

metrics_df = pd.DataFrame(rows)

# Consolidated Performance Matrix Table
st.markdown('<div class="section-title">📋 Consolidated Performance Matrix</div>', unsafe_allow_html=True)
show_df = metrics_df.copy()
for col in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
    if col in show_df.columns:
        show_df[col] = pd.to_numeric(show_df[col], errors="coerce").round(4)

# Format column headers for premium look
show_df.columns = [c.replace("_", " ").title() for c in show_df.columns]
st.dataframe(show_df, use_container_width=True, hide_index=True)

success_df = metrics_df[metrics_df["status"] == "success"].copy()
if success_df.empty:
    st.error("No successful model training records found.")
    st.stop()

for col in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
    success_df[col] = pd.to_numeric(success_df[col], errors="coerce")

# Visualizer Section
st.markdown('<div class="section-title">📉 Dynamic Model Performance Visualizer</div>', unsafe_allow_html=True)
filt_col1, filt_col2 = st.columns(2)
with filt_col1:
    disease_filter = st.selectbox("Filter by Disease Module", options=sorted(success_df["disease"].unique()))
with filt_col2:
    metric_filter = st.selectbox("Benchmark Metric", options=["roc_auc", "f1", "accuracy", "precision", "recall"])

plot_df = success_df[success_df["disease"] == disease_filter].sort_values(metric_filter, ascending=False)

# Theme-aware Plotly Chart
fig = px.bar(
    plot_df,
    x="model",
    y=metric_filter,
    text=metric_filter,
    title=f"{disease_filter.upper()} Performance Benchmarks sorted by {metric_filter.upper()}",
    color=metric_filter,
    color_continuous_scale="Tealgrn",
)
fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
fig.update_layout(
    xaxis_tickangle=-35, 
    yaxis_range=[0, 1.15], 
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#64748b",
    margin=dict(l=40, r=40, t=60, b=80),
)
st.plotly_chart(fig, use_container_width=True)

# Optimal Model Summary
st.markdown('<div class="section-title">🏆 Optimal Model Summary</div>', unsafe_allow_html=True)

best_rows = []
for disease in sorted(success_df["disease"].unique()):
    temp = success_df[success_df["disease"] == disease].copy()
    metric = "roc_auc" if temp["roc_auc"].notna().any() else "f1"
    best = temp.sort_values(metric, ascending=False).iloc[0]
    best_rows.append(
        {
            "Disease Module": disease.title(),
            "Selected Optimal Model": best["model"],
            "Selection Strategy": f"Max {metric.upper()}",
            "Validation Score": round(float(best[metric]), 4) if pd.notna(best[metric]) else None,
        }
    )

st.dataframe(pd.DataFrame(best_rows), use_container_width=True, hide_index=True)
