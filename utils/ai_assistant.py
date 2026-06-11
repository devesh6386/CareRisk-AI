"""AI Assistant for CareRisk AI.

Uses Google Gemini (via google-genai SDK) to answer follow-up questions
about a user's risk prediction result in simple, friendly language.

API key is read from Streamlit secrets:
    st.secrets["GEMINI_API_KEY"]

If the key is missing or the API call fails, a clean fallback message is shown
instead of crashing the app.
"""

from typing import List, Dict, Any, Optional


def _build_prompt(
    question: str,
    disease_type: str,
    patient_data: Dict[str, Any],
    prediction_result: int,
    probability: float,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> str:
    """Build a structured prompt for Gemini that gives it full context."""

    # Format patient data compactly
    patient_summary = ", ".join(f"{k}: {v}" for k, v in patient_data.items())

    # Format top factors — use explanation text if present, else feature name
    factors_text = ""
    for i, f in enumerate(top_factors, 1):
        explanation = f.get("explanation") or f.get("feature", "Unknown factor")
        factors_text += f"  {i}. {explanation}\n"

    prob_pct = round(probability * 100, 1)

    prompt = f"""You are a friendly, non-clinical AI health educator assistant embedded in CareRisk AI, an educational machine learning tool.

A user just received the following prediction result:
- Disease screened: {disease_type}
- Predicted risk level: {risk_level}
- Model confidence (probability): {prob_pct}%
- Key contributing factors identified by the model:
{factors_text}
- Patient input values: {patient_summary}

The user is asking: "{question}"

IMPORTANT GUIDELINES you MUST follow:
1. Explain the ML result in simple, friendly language that a non-medical person can understand.
2. Mention the top contributing factors naturally in your response.
3. Do NOT say the user HAS or DOESN'T HAVE the disease. Use language like "your predicted risk appears..." or "the model suggests..."
4. Do NOT prescribe any medicines or treatments.
5. Do NOT give a definitive diagnosis.
6. ALWAYS recommend consulting a qualified healthcare professional.
7. Keep your response under 150 words — short, warm, and clear.
8. End with a one-sentence medical disclaimer.

Respond directly to the user's question now:"""

    return prompt


def get_ai_response(
    question: str,
    disease_type: str,
    patient_data: Dict[str, Any],
    prediction_result: int,
    probability: float,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> str:
    """Call Gemini API and return a plain-language response.

    Returns a string response (either from Gemini or a graceful fallback).
    Never raises an exception — always returns a displayable string.
    """
    import streamlit as st

    # --- Check for API key ---
    api_key: Optional[str] = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        api_key = None

    if not api_key:
        return (
            "🔒 **AI assistant is unavailable.** "
            "Add `GEMINI_API_KEY` in your Streamlit secrets to enable this feature. "
            "See `.streamlit/secrets.toml.example` for instructions."
        )

    # --- Try importing google-genai SDK ---
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return (
            "⚠️ The `google-genai` package is not installed. "
            "Please add `google-genai` to `requirements.txt` and redeploy the app."
        )

    # --- Build prompt ---
    prompt = _build_prompt(
        question=question,
        disease_type=disease_type,
        patient_data=patient_data,
        prediction_result=prediction_result,
        probability=probability,
        risk_level=risk_level,
        top_factors=top_factors,
    )

    # --- Call Gemini API ---
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=300,
            ),
        )
        text = response.text.strip()
        return text if text else _fallback_response(disease_type, risk_level, top_factors)
    except Exception as exc:
        # Log to console but show clean message in UI
        print(f"[CareRisk AI] Gemini API error: {exc}")
        return _fallback_response(disease_type, risk_level, top_factors)


def _fallback_response(
    disease_type: str,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> str:
    """Return a helpful fallback answer when Gemini is unavailable."""
    factor_texts = []
    for f in top_factors[:3]:
        explanation = f.get("explanation", "")
        if explanation:
            # Extract just the first part before "—" for brevity
            short = explanation.split("—")[0].strip()
            factor_texts.append(short)

    factors_str = ", ".join(factor_texts) if factor_texts else "several health indicators"

    level_messages = {
        "Low Risk": (
            "Your result appears **low risk** for {disease}. "
            "The model did not identify major concern areas based on the values you entered. "
            "However, maintaining a healthy lifestyle — regular check-ups, balanced diet, and exercise — is always recommended."
        ),
        "Medium Risk": (
            "Your result shows **moderate risk** for {disease}. "
            "Factors such as {factors} contributed to this result. "
            "This is a good time to discuss your health with a doctor and consider lifestyle adjustments."
        ),
        "High Risk": (
            "Your result indicates **elevated risk** for {disease}. "
            "Factors such as {factors} appear to have influenced this result. "
            "This does not mean you have the disease, but it is strongly recommended to consult a qualified healthcare professional for proper evaluation."
        ),
    }

    template = level_messages.get(risk_level, level_messages["Medium Risk"])
    message = template.format(disease=disease_type, factors=factors_str)

    disclaimer = (
        "\n\n⚠️ *This is an AI-generated educational response. "
        "CareRisk AI is not a medical device and this is not medical advice. "
        "Always consult a qualified healthcare professional.*"
    )

    return message + disclaimer
