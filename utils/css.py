import streamlit as st


def inject_custom_css():
    """Inject all custom CSS for the CareRisk AI app."""
    st.markdown(
        """
        <style>
        /* ===================================================
           Global & typography
        =================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        :root {
            --primary-gradient: linear-gradient(135deg, #0f766e 0%, #0284c7 50%, #6d28d9 100%);
            --card-radius: 20px;
        }

        /* ===================================================
           Hero card (home page)
        =================================================== */
        .hero-card {
            padding: 3.5rem 2.5rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #0f766e 0%, #0284c7 50%, #6d28d9 100%);
            color: #ffffff !important;
            margin-bottom: 2.5rem;
            box-shadow: 0 20px 40px rgba(2, 132, 199, 0.18);
            text-align: center;
        }

        .hero-card h1 {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 0.8rem !important;
            border: none !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        }

        .hero-card p {
            font-size: 1.25rem !important;
            color: rgba(255, 255, 255, 0.95) !important;
            max-width: 800px;
            margin: 0 auto !important;
            line-height: 1.6 !important;
        }

        /* ===================================================
           Section titles
        =================================================== */
        .section-title {
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1.5rem !important;
            color: var(--text-color) !important;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        /* ===================================================
           Metric cards (home page counters)
        =================================================== */
        .metric-card {
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            border-radius: var(--card-radius);
            padding: 1.75rem;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 35px rgba(0, 0, 0, 0.12);
            border-color: #0284c7 !important;
        }

        .metric-card h3 {
            margin: 0 !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-card p {
            margin: 0.5rem 0 0 0 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: var(--text-color) !important;
        }

        /* ===================================================
           Feature cards
        =================================================== */
        /* Coordinate the hover state on the column container so card + button lift in unison */
        div[data-testid="column"]:has(.feature-card) {
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        div[data-testid="column"]:has(.feature-card):hover {
            transform: translateY(-6px) !important;
        }

        .feature-card {
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            border-radius: var(--card-radius);
            padding: 2rem;
            height: 100%;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        .feature-card:hover {
            box-shadow: 0 20px 35px rgba(0, 0, 0, 0.12);
            border-color: #0284c7 !important;
        }

        .feature-card h3 {
            margin: 0 0 1rem 0 !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: var(--text-color) !important;
        }

        .feature-card p {
            font-size: 1rem !important;
            line-height: 1.6 !important;
            color: var(--text-color) !important;
            opacity: 0.85;
            margin: 0 !important;
        }

        /* Cohesive button styling inside the column */
        div:has(> .feature-card) + div:has(> [data-testid="stPageLink"]) {
            margin-top: -0.5rem !important;
        }

        div:has(> .feature-card) + div:has(> [data-testid="stPageLink"]) a {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: linear-gradient(135deg, #0f766e 0%, #0284c7 100%) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 0.8rem 1.5rem !important;
            border-radius: 14px !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.15) !important;
        }

        div:has(> .feature-card) + div:has(> [data-testid="stPageLink"]) a:hover {
            background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important;
            box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25) !important;
            color: #ffffff !important;
        }

        /* ===================================================
           Risk result card — coloured left border
        =================================================== */
        .risk-card {
            padding: 2rem 2.4rem;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            margin-bottom: 1.5rem;
            transition: transform 0.25s ease;
        }

        .risk-card:hover {
            transform: translateY(-2px);
        }

        .risk-card h2 {
            margin: 0 0 0.5rem 0 !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        .risk-card p {
            margin: 0.4rem 0 !important;
            font-size: 1.1rem !important;
            color: var(--text-color) !important;
        }

        /* ===================================================
           Risk factor cards — inline readable explanations
        =================================================== */
        .factor-card {
            margin-bottom: 0.85rem;
            background-color: var(--secondary-background-color);
            padding: 0.85rem 1.2rem;
            border-radius: 14px;
            border-left: 4px solid #0ea5e9;
            transition: border-color 0.2s ease;
        }

        .factor-card:hover {
            border-left-color: #8b5cf6;
        }

        .factor-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            color: white;
            font-weight: 700;
            font-size: 0.75rem;
            border-radius: 50%;
            margin-right: 0.5rem;
            flex-shrink: 0;
            vertical-align: middle;
        }

        .factor-text {
            font-size: 0.93rem;
            line-height: 1.55;
            color: var(--text-color);
        }

        /* ===================================================
           AI Assistant section
        =================================================== */
        .ai-section {
            background: linear-gradient(135deg,
                rgba(99, 102, 241, 0.06) 0%,
                rgba(139, 92, 246, 0.06) 100%);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 20px;
            padding: 1.8rem 2rem;
            margin-top: 2rem;
        }

        .ai-section-title {
            font-size: 1.5rem !important;
            font-weight: 700;
            color: var(--text-color) !important;
            margin-bottom: 0.5rem;
        }

        .ai-response-box {
            background-color: var(--background-color) !important;
            border: 1px solid rgba(139, 92, 246, 0.25);
            border-radius: 14px;
            padding: 1.2rem 1.5rem;
            margin-top: 1rem;
            line-height: 1.65;
            font-size: 0.97rem;
        }

        /* ===================================================
           Example question chips
        =================================================== */
        .question-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.75rem 0 1rem 0;
        }

        .question-chip {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(139, 92, 246, 0.12));
            border: 1px solid rgba(139, 92, 246, 0.25);
            border-radius: 999px;
            padding: 0.3rem 0.85rem;
            font-size: 0.82rem;
            color: var(--text-color);
            cursor: default;
            transition: background 0.2s ease;
        }

        /* ===================================================
           Disclaimer box
        =================================================== */
        .disclaimer-box {
            background-color: rgba(239, 68, 68, 0.06) !important;
            border: 1px solid rgba(239, 68, 68, 0.18) !important;
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin: 2rem 0;
            color: var(--text-color) !important;
        }

        .disclaimer-box p {
            margin: 0 !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }

        /* ===================================================
           Footer
        =================================================== */
        .footer {
            margin-top: 5rem;
            padding: 2.5rem;
            border-top: 1px solid var(--secondary-background-color) !important;
            text-align: center;
            font-size: 0.95rem !important;
            color: var(--text-color) !important;
            opacity: 0.7;
            line-height: 1.6;
        }

        /* ===================================================
           Responsive
        =================================================== */
        @media (max-width: 768px) {
            .hero-card { padding: 2.5rem 1.5rem; border-radius: 16px; }
            .hero-card h1 { font-size: 2.5rem !important; }
            .hero-card p  { font-size: 1.1rem !important; }
            .metric-card  { padding: 1.25rem; }
            .metric-card h3 { font-size: 2rem !important; }
            .feature-card { padding: 1.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
