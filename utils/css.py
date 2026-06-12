import streamlit as st

def inject_custom_css():
    """Inject all custom CSS for the CareRisk AI app."""
    st.markdown(
        """
        <style>
        /* ===================================================
           Global & Typography (Healthcare SaaS Theme)
        =================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        :root {
            --primary-blue: #2563eb;
            --primary-teal: #0f766e;
            --primary-purple: #7c3aed;
            --bg-color: var(--background-color);
            --text-dark: var(--text-color);
            --text-muted: gray;
            --card-white: var(--secondary-background-color);
            --card-radius: 16px;
        }

        /* Ensure Streamlit containers take less empty space */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1100px !important; /* Centered max-width container */
        }

        /* ===================================================
           Sidebar Styling
        =================================================== */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background-color) !important;
            border-right: 1px solid rgba(128, 128, 128, 0.2) !important;
        }

        .sidebar-card {
            background-color: var(--background-color) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            text-align: center;
        }

        /* ===================================================
           Hero Section (Homepage)
        =================================================== */
        .hero-section {
            padding: 4rem 2.5rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(37,99,235,0.95) 0%, rgba(15,118,110,0.95) 100%), 
                        url('https://www.transparenttextures.com/patterns/cubes.png');
            color: #ffffff !important;
            margin-bottom: 3rem;
            box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.25);
            text-align: center;
            backdrop-filter: blur(10px); /* Glassmorphism */
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 1rem !important;
            letter-spacing: -0.025em;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .hero-subtitle {
            font-size: 1.25rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
            max-width: 750px;
            margin: 0 auto 2rem auto !important;
            line-height: 1.6 !important;
            font-weight: 400 !important;
        }

        /* Hero buttons injected via st.button or st.page_link will be styled generally, 
           but we can target them if wrapped nicely */

        /* ===================================================
           Section Titles
        =================================================== */
        .section-title {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            margin-top: 3rem !important;
            margin-bottom: 1.5rem !important;
            color: var(--text-dark) !important;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(128, 128, 128, 0.2);
        }

        /* ===================================================
           Metric Cards
        =================================================== */
        .metric-card {
            background-color: var(--card-white) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: left;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: var(--primary-blue) !important;
        }

        .metric-card h3 {
            margin: 0 !important;
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: var(--primary-blue) !important;
            line-height: 1;
        }

        .metric-card p.title {
            margin: 0 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: var(--text-dark) !important;
        }

        .metric-card p.desc {
            margin: 0 !important;
            font-size: 0.875rem !important;
            color: var(--text-muted) !important;
            line-height: 1.4;
        }

        /* ===================================================
           Disease Cards & CTA Buttons
        =================================================== */
        .disease-card {
            background-color: var(--card-white) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            border-radius: var(--card-radius);
            padding: 2rem;
            height: 100%;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease !important;
            display: flex;
            flex-direction: column;
        }

        div[data-testid="column"]:has(.disease-card):hover {
            transform: translateY(-6px) !important;
        }

        div[data-testid="column"]:has(.disease-card):hover .disease-card {
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
            border-color: var(--primary-blue) !important;
        }

        .disease-card h3 {
            margin: 0 0 0.75rem 0 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: var(--text-dark) !important;
        }

        .disease-card p {
            font-size: 1rem !important;
            line-height: 1.6 !important;
            color: var(--text-muted) !important;
            margin-bottom: 1.5rem !important;
            flex-grow: 1;
        }

        .disease-tag {
            display: inline-block;
            background-color: rgba(128, 128, 128, 0.15);
            color: var(--text-dark);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }

        /* St.page_link styling inside disease columns */
        div:has(> .disease-card) + div:has(> [data-testid="stPageLink"]) {
            margin-top: -1rem !important;
        }

        div:has(> .disease-card) + div:has(> [data-testid="stPageLink"]) a {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: var(--primary-blue) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
            border-radius: 12px !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        }

        div:has(> .disease-card) + div:has(> [data-testid="stPageLink"]) a:hover {
            background-color: #1d4ed8 !important; /* darker blue */
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
            color: #ffffff !important;
        }

        /* Global primary button styling for st.button / st.page_link where applicable */
        .cta-button button, .cta-button a {
            background-color: var(--primary-teal) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: none !important;
        }
        
        .cta-button button:hover, .cta-button a:hover {
            background-color: #0f766e !important;
        }

        /* ===================================================
           Prediction Pages (Risk Cards & Form Cards)
        =================================================== */
        [data-testid="stForm"] {
            background-color: var(--card-white) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }

        .risk-card {
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            background-color: var(--card-white) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            margin-bottom: 2rem;
        }

        .risk-card h2 {
            margin: 0 0 0.5rem 0 !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em;
        }

        .risk-card p {
            margin: 0.5rem 0 !important;
            font-size: 1.15rem !important;
            color: var(--text-dark) !important;
        }

        .factor-card {
            margin-bottom: 1rem;
            background-color: var(--background-color);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border-left: 5px solid var(--primary-blue);
            border-top: 1px solid rgba(128, 128, 128, 0.2);
            border-right: 1px solid rgba(128, 128, 128, 0.2);
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .factor-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            background-color: var(--primary-blue);
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .factor-text {
            font-size: 1rem;
            line-height: 1.5;
            color: var(--text-dark);
            font-weight: 500;
        }

        /* ===================================================
           AI Assistant & Disclaimers
        =================================================== */
        .ai-section {
            background-color: rgba(139, 92, 246, 0.05) !important; /* subtle purple */
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2.5rem;
        }

        .ai-section-title {
            font-size: 1.5rem !important;
            font-weight: 700;
            color: var(--primary-purple) !important;
            margin-bottom: 0.75rem;
        }

        .ai-response-box {
            background-color: var(--card-white) !important;
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            line-height: 1.7;
            font-size: 1rem;
            color: var(--text-dark) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .question-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 1rem 0;
        }

        .question-chip {
            background-color: var(--card-white);
            border: 1px solid rgba(139, 92, 246, 0.4);
            border-radius: 9999px;
            padding: 0.4rem 1rem;
            font-size: 0.875rem;
            color: var(--primary-purple);
            font-weight: 500;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .disclaimer-box {
            background-color: rgba(239, 68, 68, 0.05) !important; /* subtle red */
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 2.5rem 0 1rem 0;
            color: #ef4444 !important; /* solid red text */
        }

        .disclaimer-box p {
            margin: 0 !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            font-weight: 500;
        }

        /* ===================================================
           Footer
        =================================================== */
        .footer {
            margin-top: 4rem;
            padding: 2rem;
            border-top: 1px solid rgba(128, 128, 128, 0.2) !important;
            text-align: center;
            font-size: 0.875rem !important;
            color: var(--text-muted) !important;
            line-height: 1.6;
        }

        /* Make Streamlit buttons primary blue when inside our forms */
        div.stButton > button {
            background-color: var(--primary-blue) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
        }
        
        div.stDownloadButton > button {
            background-color: var(--background-color) !important;
            color: var(--text-dark) !important;
            border: 1px solid rgba(128, 128, 128, 0.4) !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
        }
        div.stDownloadButton > button:hover {
            background-color: rgba(128, 128, 128, 0.1) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
