"""AI Assistant for CareRisk AI — Dynamic, question-aware Gemini integration.

API key is read from Streamlit secrets:
    st.secrets["GEMINI_API_KEY"]

No responses are cached. Every question produces a fresh, contextual answer
based on the exact question asked, the patient's input values, and the
ML prediction result.
"""

from typing import List, Dict, Any, Optional, Tuple


def _format_patient_data(patient_data: Dict[str, Any]) -> str:
    """Format patient data as a clean, readable bullet list."""
    lines = []
    for k, v in patient_data.items():
        # Make key name more readable (replace underscores with spaces, title-case)
        readable_key = k.replace("_", " ").title()
        lines.append(f"  • {readable_key}: {v}")
    return "\n".join(lines)


def _format_top_factors(top_factors: List[Dict[str, Any]]) -> str:
    """Format top risk factors as a numbered readable list."""
    if not top_factors:
        return "  • No specific factors identified."
    lines = []
    for i, f in enumerate(top_factors, 1):
        explanation = f.get("explanation") or f.get("feature", "Unknown factor")
        lines.append(f"  {i}. {explanation}")
    return "\n".join(lines)


def _build_prompt(
    question: str,
    disease_type: str,
    patient_data: Dict[str, Any],
    prediction_result: int,
    probability: float,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> str:
    """Build a rich, contextual prompt so Gemini gives question-specific answers."""

    prob_pct = round(probability * 100, 1)
    prediction_label = "Positive (at risk)" if prediction_result else "Negative (low risk)"

    patient_summary = _format_patient_data(patient_data)
    factors_summary = _format_top_factors(top_factors)

    prompt = f"""You are CareRisk AI, a helpful healthcare ML explanation assistant embedded in an educational app.

--- PATIENT PREDICTION CONTEXT ---
Disease Screened: {disease_type}
Risk Level: {risk_level}
Risk Probability: {prob_pct}%
Prediction Result: {prediction_label}

Patient Input Values:
{patient_summary}

Top Risk Factors identified by the ML model:
{factors_summary}
--- END OF CONTEXT ---

User Question:
"{question}"

--- ANSWER RULES (follow every rule strictly) ---
1. Answer the EXACT question asked. Do not give a generic response.
2. If the question is general (e.g., "what is diabetes?"), answer it generally without using patient values.
3. If the question is personal (e.g., "why am I high risk?"), use the patient values and top risk factors in your explanation.
4. If the question asks how to reduce risk, give practical lifestyle suggestions ONLY (diet, exercise, sleep, stress management). Do NOT suggest or name any medicines.
5. Explain in simple, friendly, beginner-level language. Avoid medical jargon.
6. Do NOT say the patient "has" or "does not have" the disease. Use language like "your predicted risk appears..." or "the model suggests..."
7. Do NOT prescribe, recommend, or name any medication.
8. Always recommend consulting a qualified doctor or healthcare professional.
9. Keep your response under 120 words — concise and clear.
10. End with exactly one sentence medical disclaimer starting with "⚠️ Disclaimer:"

Now answer the user's question:"""

    return prompt


def get_ai_response(
    question: str,
    disease_type: str,
    patient_data: Dict[str, Any],
    prediction_result: int,
    probability: float,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> Tuple[str, Optional[str]]:
    """Call Gemini API and return a dynamic, question-specific response.

    Returns:
        Tuple of (user_message: str, technical_error: Optional[str])
        - user_message: Clean message for display on the UI.
        - technical_error: Raw error string if API failed, else None.
          Show this inside a st.expander for developers.
    """
    import streamlit as st

    # --- 1. Check for API key ---
    api_key: Optional[str] = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        api_key = None

    if not api_key:
        return (
            "🔒 **AI assistant is not configured.**\n\n"
            "To enable AI explanations, add your `GEMINI_API_KEY` to `.streamlit/secrets.toml`.\n"
            "See `.streamlit/secrets.toml.example` for the format.",
            None,
        )

    # --- 2. Try importing the SDK ---
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return (
            "⚠️ The `google-genai` package is not installed in this environment.\n"
            "Please run `pip install google-genai` and restart the app.",
            "ImportError: google-genai not installed",
        )

    # --- 3. Build the dynamic prompt ---
    prompt = _build_prompt(
        question=question,
        disease_type=disease_type,
        patient_data=patient_data,
        prediction_result=prediction_result,
        probability=probability,
        risk_level=risk_level,
        top_factors=top_factors,
    )

    # --- 4. Call Gemini with question-tuned generation config ---
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                temperature=0.7,       # More creative / varied responses
                top_p=0.9,            # Nucleus sampling for diversity
                max_output_tokens=250, # Enough for a full, detailed answer
            ),
        )
        text = response.text.strip() if response.text else ""
        if text:
            return text, None
        else:
            return (
                "🤔 The AI returned an empty response. Please try rephrasing your question.",
                "Gemini returned empty response.text",
            )

    except Exception as exc:
        # Return a clean UI message + the real error for developers
        technical_error = f"{type(exc).__name__}: {exc}"
        user_message = (
            "⚠️ **AI assistant encountered an error.**\n\n"
            "The response could not be generated right now. "
            "Please check your API key or try again in a moment.\n\n"
            "💡 *Expand the technical details below for the error message.*"
        )
        return user_message, technical_error
