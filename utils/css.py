import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Modern theme colors and layout styles */
        :root {
            --primary-gradient: linear-gradient(135deg, #0f766e 0%, #0284c7 50%, #6d28d9 100%);
        }
        
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

        .metric-card {
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            border-radius: 20px;
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

        .feature-card {
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            border-radius: 20px;
            padding: 2rem;
            height: 100%;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 35px rgba(0, 0, 0, 0.12);
            border-color: #0284c7 !important;
        }
        
        .feature-card h3 {
            margin: 0 0 1rem 0 !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: var(--text-color) !important;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        
        .feature-card p {
            font-size: 1rem !important;
            line-height: 1.6 !important;
            color: var(--text-color) !important;
            opacity: 0.85;
            margin: 0 !important;
        }

        .risk-card {
            padding: 2.2rem;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
            background-color: var(--background-color) !important;
            border: 1px solid var(--secondary-background-color) !important;
            margin-bottom: 2rem;
            transition: transform 0.3s ease;
        }
        
        .risk-card:hover {
            transform: translateY(-2px);
        }
        
        .risk-card h2 {
            margin: 0 0 1rem 0 !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        .risk-card p {
            margin: 0.5rem 0 !important;
            font-size: 1.15rem !important;
            color: var(--text-color) !important;
        }

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

        @media (max-width: 768px) {
            .hero-card {
                padding: 2.5rem 1.5rem;
                border-radius: 16px;
            }
            .hero-card h1 {
                font-size: 2.5rem !important;
            }
            .hero-card p {
                font-size: 1.1rem !important;
            }
            .metric-card {
                padding: 1.25rem;
            }
            .metric-card h3 {
                font-size: 2rem !important;
            }
            .feature-card {
                padding: 1.5rem;
            }
            .feature-card h3 {
                font-size: 1.25rem !important;
                flex-direction: column;
                text-align: center;
            }
            .feature-card p {
                text-align: center;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
