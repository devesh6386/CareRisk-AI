import streamlit as st
from pathlib import Path


def inject_custom_css():
    """Inject all custom CSS for the CareRisk AI app.

    Ensures perfect light/dark theme contrast, premium card aesthetics,
    and responsive layouts on desktop, tablet, and mobile.
    """
    st.markdown(
        """
        <style>
        /* ===================================================
           Global Font & Variables
        =================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        :root {
            --primary-gradient: linear-gradient(135deg, #0f766e 0%, #2563eb 50%, #7c3aed 100%);
            --blue-color: #2563eb;
            --teal-color: #0f766e;
            --purple-color: #7c3aed;
            --dark-text: #1e293b;
            --light-bg: #f8fafc;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            --card-hover-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1), 0 4px 6px -2px rgba(37, 99, 235, 0.05);
        }

        /* ===================================================
           Hero Section (Homepage)
        =================================================== */
        .hero-section {
            padding: 3.5rem 2.5rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #0f766e 0%, #2563eb 50%, #7c3aed 100%);
            color: #ffffff !important;
            margin-bottom: 2.5rem;
            box-shadow: 0 20px 40px rgba(37, 99, 235, 0.15);
            text-align: center;
        }

        .hero-title {
            font-size: 2.75rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 0.8rem !important;
            border: none !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .hero-subtitle {
            font-size: 1.15rem !important;
            color: rgba(255, 255, 255, 0.95) !important;
            max-width: 800px;
            margin: 0 auto !important;
            line-height: 1.6 !important;
        }

        /* ===================================================
           Section Titles
        =================================================== */
        .section-title {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            color: var(--teal-color) !important;
            border-bottom: 2px solid #e2e8f0 !important;
            padding-bottom: 0.5rem !important;
        }

        /* ===================================================
           General Form & Card Styles
        =================================================== */
        /* Streamlit Forms */
        div[data-testid="stForm"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            box-shadow: var(--card-shadow) !important;
        }

        /* Form Labels & Text Visibility Fixes */
        div[data-testid="stForm"] label, 
        div[data-testid="stForm"] p, 
        div[data-testid="stForm"] span, 
        div[data-testid="stForm"] legend,
        div[data-testid="stForm"] div[data-testid="stMarkdownContainer"] p {
            color: var(--dark-text) !important;
            font-weight: 500 !important;
        }

        /* ===================================================
           Disease Cards (Homepage)
        =================================================== */
        .disease-card-wrapper {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            box-shadow: var(--card-shadow) !important;
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1.5rem;
        }

        .disease-card-wrapper:hover {
            transform: translateY(-5px);
            box-shadow: var(--card-hover-shadow) !important;
            border-color: var(--blue-color) !important;
        }

        .disease-card-body {
            padding: 2rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        .disease-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .disease-card-body h3 {
            margin: 0 0 0.75rem 0 !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }

        .disease-card-body p {
            color: #475569 !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            margin-bottom: 1.25rem !important;
            flex-grow: 1;
        }

        .disease-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: auto;
        }

        .disease-tag {
            background-color: #f1f5f9 !important;
            color: #475569 !important;
            padding: 0.25rem 0.75rem !important;
            border-radius: 9999px !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }

        /* Style page link buttons flush with bottom of cards */
        .disease-card-wrapper div[data-testid="stPageLink"] {
            margin: 0 !important;
            padding: 0 !important;
        }

        .disease-card-wrapper div[data-testid="stPageLink"] a {
            border-radius: 0 !important;
            border: none !important;
            border-top: 1px solid #e2e8f0 !important;
            background-color: #f8fafc !important;
            color: var(--teal-color) !important;
            padding: 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            text-align: center !important;
            justify-content: center !important;
        }

        .disease-card-wrapper:hover div[data-testid="stPageLink"] a {
            background: linear-gradient(135deg, #0f766e 0%, #2563eb 100%) !important;
            color: #ffffff !important;
        }

        /* ===================================================
           Dashboard Metric Cards
        =================================================== */
        .metric-card {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            box-shadow: var(--card-shadow) !important;
            transition: all 0.3s ease !important;
            height: 100% !important;
            color: var(--dark-text) !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--card-hover-shadow) !important;
            border-color: var(--blue-color) !important;
        }

        .metric-card h3 {
            margin: 0.5rem 0 !important;
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, var(--teal-color), var(--blue-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-card h4 {
            margin: 0.25rem 0 !important;
            color: var(--teal-color) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }

        .metric-card p {
            margin: 0 !important;
            font-size: 0.9rem !important;
            color: #64748b !important;
            line-height: 1.4 !important;
        }

        /* ===================================================
           Risk Results Layout (Prediction Pages)
        =================================================== */
        .risk-card {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 1.75rem !important;
            box-shadow: var(--card-shadow) !important;
            margin-bottom: 1.25rem !important;
            color: var(--dark-text) !important;
        }

        .risk-card h2 {
            margin: 0 0 0.5rem 0 !important;
            font-size: 1.75rem !important;
            font-weight: 800 !important;
        }

        .risk-card p {
            margin: 0.5rem 0 0 0 !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
            color: #475569 !important;
        }

        /* Numbered Key Risk Factors */
        .factor-card {
            margin-bottom: 0.75rem;
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            padding: 0.9rem 1.25rem;
            border-radius: 14px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
            border-left: 5px solid var(--blue-color) !important;
        }

        .factor-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, var(--blue-color), var(--purple-color));
            color: white !important;
            font-weight: 700;
            font-size: 0.8rem;
            border-radius: 50%;
            margin-right: 0.75rem;
            flex-shrink: 0;
        }

        .factor-text {
            font-size: 0.92rem;
            line-height: 1.5;
            color: var(--dark-text) !important;
            font-weight: 500 !important;
        }

        /* ===================================================
           AI Chatbot Layout ("Ask CareRisk AI")
        =================================================== */
        .ai-section {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 1.75rem !important;
            margin-top: 1.5rem !important;
            box-shadow: var(--card-shadow) !important;
            color: var(--dark-text) !important;
        }

        .ai-section-title {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: var(--purple-color) !important;
            margin-bottom: 0.5rem !important;
        }

        .ai-response-box {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-left: 4px solid var(--purple-color) !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            margin-top: 1rem !important;
            color: var(--dark-text) !important;
            line-height: 1.6 !important;
            font-size: 0.95rem !important;
        }

        .question-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.75rem 0 1.25rem 0;
        }

        .question-chip {
            background-color: #f1f5f9 !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 999px !important;
            padding: 0.35rem 0.85rem !important;
            font-size: 0.82rem !important;
            color: #475569 !important;
            font-weight: 500 !important;
            transition: all 0.2s ease;
        }

        .question-chip:hover {
            background-color: #e2e8f0 !important;
            color: var(--dark-text) !important;
        }

        /* ===================================================
           About & Documentation Portfolio Cards
        =================================================== */
        .about-card {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            box-shadow: var(--card-shadow) !important;
            margin-bottom: 1.5rem !important;
            color: var(--dark-text) !important;
        }

        .about-card h3 {
            color: var(--teal-color) !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            border-bottom: 1px solid #f1f5f9 !important;
            padding-bottom: 0.5rem !important;
        }

        .about-card p, .about-card li {
            color: #475569 !important;
            line-height: 1.6 !important;
            font-size: 0.98rem !important;
        }

        /* ===================================================
           Sidebar Styling
        =================================================== */
        .sidebar-header {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.05) 0%, rgba(37, 99, 235, 0.05) 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .sidebar-title {
            font-size: 1.35rem !important;
            font-weight: 800 !important;
            color: var(--teal-color) !important;
            margin: 0.5rem 0 0.25rem 0 !important;
        }

        .sidebar-tagline {
            font-size: 0.8rem !important;
            color: #64748b !important;
            margin: 0 !important;
            font-weight: 500 !important;
        }

        .sidebar-badge {
            background-color: #eff6ff !important;
            border: 1px solid #bfdbfe !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.85rem !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1.5rem !important;
        }

        .badge-icon {
            font-size: 1rem;
        }

        .badge-text {
            color: #1e3a8a !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }

        /* ===================================================
           Alerts & Disclaimer Box
        =================================================== */
        .disclaimer-box {
            background-color: rgba(239, 68, 68, 0.04) !important;
            border: 1px solid rgba(239, 68, 68, 0.15) !important;
            border-radius: 16px !important;
            padding: 1.25rem 1.5rem !important;
            margin: 1.5rem 0 !important;
            color: #7f1d1d !important;
        }

        .disclaimer-box p {
            margin: 0 !important;
            font-size: 0.9rem !important;
            line-height: 1.5 !important;
            color: #7f1d1d !important;
        }

        .footer {
            margin-top: 4rem;
            padding: 2rem;
            border-top: 1px solid #e2e8f0 !important;
            text-align: center;
            font-size: 0.88rem !important;
            color: #64748b !important;
        }

        /* ===================================================
           Responsive Media Queries
        =================================================== */
        @media (max-width: 768px) {
            .hero-section {
                padding: 2.5rem 1.5rem;
                border-radius: 16px;
            }
            .hero-title {
                font-size: 2rem !important;
            }
            .hero-subtitle {
                font-size: 1rem !important;
            }
            div[data-testid="stForm"] {
                padding: 1.25rem !important;
            }
            /* Make Streamlit buttons fill container on mobile */
            div[data-testid="stForm"] button, 
            div[data-testid="stPageLink"] a {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the unified sidebar with logo, branding, and disclaimer."""
    BASE_DIR = Path(__file__).resolve().parents[1]
    LOGO_PATH = BASE_DIR / "assets" / "logo.png"

    with st.sidebar:
        # Title Card
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        st.markdown('<h2 class="sidebar-title">🩺 CareRisk AI</h2>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-tagline">Clinical Risk Intelligence Platform</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Disclaimer Badge
        st.markdown(
            """
            <div class="sidebar-badge">
                <span class="badge-icon">ℹ️</span>
                <span class="badge-text">Educational Demo Only</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
