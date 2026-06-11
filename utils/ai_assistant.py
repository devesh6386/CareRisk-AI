"""AI Assistant for CareRisk AI — Groq API integration.

API key is read from Streamlit secrets:
    st.secrets.get("GROQ_API_KEY")

No responses are cached. Every question produces a fresh, contextual answer
based on the exact question asked, the patient's input values, and the
ML prediction result.
"""

from typing import List, Dict, Any, Optional, Union
import streamlit as st
from groq import Groq


def _format_patient_data(patient_data: Any) -> str:
    """Format patient data as a clean, readable bullet list."""
    if not isinstance(patient_data, dict):
        return str(patient_data)
    lines = []
    for k, v in patient_data.items():
        # Make key name more readable (replace underscores with spaces, title-case)
        readable_key = str(k).replace("_", " ").title()
        lines.append(f"  • {readable_key}: {v}")
    return "\n".join(lines)


def _format_top_factors(top_factors: Any) -> str:
    """Format top risk factors as a numbered readable list."""
    if not isinstance(top_factors, list):
        return str(top_factors)
    if not top_factors:
        return "  • No specific factors identified."
    lines = []
    for i, f in enumerate(top_factors, 1):
        if isinstance(f, dict):
            explanation = f.get("explanation") or f.get("feature", "Unknown factor")
        else:
            explanation = str(f)
        lines.append(f"  {i}. {explanation}")
    return "\n".join(lines)


def get_ai_response(
    question: str,
    disease_type: str,
    patient_data: Any,
    prediction_result: Any,
    probability: Any,
    risk_level: str,
    top_factors: Any,
) -> str:
    """Call Groq API and return a dynamic, question-specific response.

    Returns:
        String containing the AI explanation or an error/unavailable message.
    """
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "AI assistant is unavailable. Please add GROQ_API_KEY in Streamlit secrets."

    # Format probability if it's a float/decimal
    prob_val = probability
    if isinstance(prob_val, (int, float)):
        if prob_val <= 1.0:
            prob_val = round(prob_val * 100, 1)
        else:
            prob_val = round(prob_val, 1)

    patient_summary = _format_patient_data(patient_data)
    factors_summary = _format_top_factors(top_factors)

    try:
        client = Groq(api_key=api_key)

        prompt = f"""You are CareRisk AI, a helpful healthcare ML explanation assistant.

Disease: {disease_type}
Prediction Result: {prediction_result}
Risk Level: {risk_level}
Risk Probability: {prob_val}%

Patient Inputs:
{patient_summary}

Top Risk Factors:
{factors_summary}

User Question:
{question}

Rules:
* Answer the exact question asked.
* Use patient values only when relevant.
* Do not repeat same generic response.
* Do not diagnose disease.
* Do not prescribe medicines.
* Give simple lifestyle guidance only.
* Keep answer under 120 words.
* Be friendly and clear.
* End with a short medical disclaimer."""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_tokens=250,
        )

        answer = completion.choices[0].message.content
        if answer:
            return answer.strip()
        else:
            return "🤔 The AI returned an empty response. Please try rephrasing your question."

    except Exception as e:
        return f"AI response failed. Please check your Groq API key or billing. Error: {str(e)}"
