"""PDF report generation for CareRisk AI.

Generates a professional, user-friendly PDF report for each prediction.
Raw SHAP values and model internals are NOT included — only readable output.
"""

from datetime import datetime
from io import BytesIO
from typing import Dict, List, Any

from fpdf import FPDF


class CareRiskPDF(FPDF):
    """Custom PDF class with branded header and footer."""

    def header(self):
        # Teal accent bar at top
        self.set_fill_color(15, 118, 110)   # teal-700
        self.rect(0, 0, 210, 12, "F")
        # Title text on accent bar
        self.set_font("Arial", "B", 13)
        self.set_text_color(255, 255, 255)
        self.set_y(2)
        self.cell(0, 8, "CareRisk AI  |  Health Risk Assessment Report", ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.multi_cell(
            0,
            5,
            "DISCLAIMER: CareRisk AI is an educational ML project. "
            "This report is NOT medical advice. Always consult a qualified healthcare professional.",
            align="C",
        )
        self.set_text_color(0, 0, 0)

    def section_title(self, title: str):
        """Styled section heading."""
        self.ln(4)
        self.set_fill_color(240, 249, 255)   # light blue-50
        self.set_font("Arial", "B", 11)
        self.set_text_color(2, 132, 199)     # sky-600
        self.cell(0, 9, f"  {title}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def key_value(self, label: str, value: str):
        """Bold label + normal value on one line."""
        self.set_font("Arial", "B", 10)
        label_w = 60
        self.cell(label_w, 7, _safe_text(label + ":"))
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 7, _safe_text(value))


def _safe_text(value: Any) -> str:
    """FPDF with Arial works best with Latin-1 text — strip unsupported chars."""
    return str(value).encode("latin-1", errors="ignore").decode("latin-1")


def _risk_color_rgb(risk_level: str):
    """Return (R, G, B) for a risk level."""
    mapping = {
        "Low Risk":    (22, 163, 74),    # green-600
        "Medium Risk": (245, 158, 11),   # amber-500
        "High Risk":   (220, 38, 38),    # red-600
    }
    return mapping.get(risk_level, (100, 116, 139))


def generate_report(
    patient_data: Dict[str, Any],
    disease_type: str,
    prediction: int,
    probability: float,
    risk_level: str,
    top_factors: List[Dict[str, Any]],
) -> bytes:
    """Generate a downloadable PDF report and return raw bytes.

    Parameters
    ----------
    patient_data  : raw user-entered values (key-value dict)
    disease_type  : "Diabetes", "Heart Disease", or "Stroke"
    prediction    : int class (0 or 1) — not shown to user directly
    probability   : float 0-1
    risk_level    : "Low Risk" / "Medium Risk" / "High Risk"
    top_factors   : list of dicts with 'feature' and 'explanation' keys
    """
    pdf = CareRiskPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ------------------------------------------------------------------
    # Meta section
    # ------------------------------------------------------------------
    pdf.section_title("Report Information")
    pdf.key_value("Generated On", datetime.now().strftime("%B %d, %Y at %H:%M"))
    pdf.key_value("Disease Module", disease_type)
    pdf.key_value("Report Type", "ML Risk Screening Summary")
    pdf.ln(3)

    # ------------------------------------------------------------------
    # Risk result section — coloured heading
    # ------------------------------------------------------------------
    pdf.section_title("Predicted Risk Result")
    r, g, b = _risk_color_rgb(risk_level)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 12, f"  {risk_level}", ln=True)
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"  Model Confidence: {probability * 100:.1f}%", ln=True)

    # Visual probability bar (ASCII-style, PDF-friendly)
    filled = int(probability * 30)
    bar = "[" + "#" * filled + "-" * (30 - filled) + "]"
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 7, f"  {bar}  {probability * 100:.1f}%", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Risk interpretation
    pdf.set_font("Arial", "I", 10)
    risk_messages = {
        "Low Risk":    "The model did not identify significant risk indicators. Maintain healthy habits and attend regular check-ups.",
        "Medium Risk": "Some risk factors were identified. Consider consulting a healthcare professional for a thorough evaluation.",
        "High Risk":   "Several risk factors were flagged. It is advisable to consult a qualified healthcare professional promptly.",
    }
    pdf.set_fill_color(245, 245, 245)
    pdf.multi_cell(0, 6, f"  {risk_messages.get(risk_level, '')}", fill=True)
    pdf.ln(3)

    # ------------------------------------------------------------------
    # Patient input values
    # ------------------------------------------------------------------
    pdf.section_title("Patient-Entered Health Values")
    pdf.set_font("Arial", "", 10)
    for key, value in patient_data.items():
        pdf.key_value(key, str(value))
    pdf.ln(3)

    # ------------------------------------------------------------------
    # Important risk factors (human-readable, no SHAP numbers)
    # ------------------------------------------------------------------
    pdf.section_title("Key Risk Factors Identified by the Model")
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "  (Factors are listed in order of model importance. No raw numbers are shown.)", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    if top_factors:
        for i, item in enumerate(top_factors, 1):
            explanation = item.get("explanation") or item.get("feature", "Unknown factor")
            pdf.set_font("Arial", "B", 10)
            # Number badge
            pdf.set_fill_color(2, 132, 199)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(8, 7, f"{i}", fill=True, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(255, 255, 255)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 7, f"  {_safe_text(explanation)}")
            pdf.ln(1)
    else:
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 7, "  No factor information available.", ln=True)

    # ------------------------------------------------------------------
    # Suggested next steps
    # ------------------------------------------------------------------
    pdf.section_title("Suggested Next Steps")
    pdf.set_font("Arial", "", 10)
    next_steps = {
        "Low Risk": [
            "Continue maintaining a healthy lifestyle with balanced nutrition and regular physical activity.",
            "Schedule routine health check-ups at least once a year.",
            "Monitor your values periodically and note any significant changes.",
        ],
        "Medium Risk": [
            "Consult a healthcare professional to discuss these results and request relevant tests.",
            "Review your diet, physical activity, and stress levels.",
            "Follow up with your doctor regularly to track changes over time.",
        ],
        "High Risk": [
            "Schedule an appointment with a qualified healthcare professional as soon as possible.",
            "Do not use this report as a diagnosis — a clinical evaluation is necessary.",
            "Bring this report to your appointment to share the risk factors identified.",
            "Take care of your mental health; a high-risk result can be stressful.",
        ],
    }
    for step in next_steps.get(risk_level, []):
        pdf.cell(6, 7, chr(149))   # bullet character
        pdf.multi_cell(0, 7, f" {_safe_text(step)}")
    pdf.ln(3)

    # ------------------------------------------------------------------
    # Medical disclaimer
    # ------------------------------------------------------------------
    pdf.section_title("Medical Disclaimer")
    pdf.set_font("Arial", "", 10)
    pdf.set_fill_color(255, 240, 240)
    pdf.multi_cell(
        0,
        6,
        "CareRisk AI is not a medical device and does not provide diagnosis, treatment, or medical advice. "
        "The prediction is generated by a machine learning model trained on publicly available datasets and "
        "may be inaccurate. Risk scores are probabilistic estimates, not certainties. "
        "Always consult a qualified and licensed healthcare professional for medical decisions.",
        fill=True,
    )

    # Return as bytes
    output = pdf.output(dest="S")
    if isinstance(output, str):
        return output.encode("latin-1", errors="ignore")
    if isinstance(output, bytearray):
        return bytes(output)
    return output
