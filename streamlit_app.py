# ============================================================
# BRANDPULSE AI
# Spotify Brand Reputation Intelligence System
# ============================================================

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import (
    analyse_predictions,
)

from src.distilbert_predictor import (
    predict_batch,
    predict_sentiment,
)

from src.llm_service import (
    MANAGER_PROVIDERS,
    MANAGER_ROLES,
    generate_executive_report,
    generate_manager_report,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BrandPulse AI",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

:root {
    --green: #1ED760;
    --green-soft: rgba(30, 215, 96, 0.14);

    --purple: #A855F7;
    --purple-soft: rgba(168, 85, 247, 0.15);

    --blue: #38BDF8;
    --blue-soft: rgba(56, 189, 248, 0.14);

    --pink: #F472B6;
    --pink-soft: rgba(244, 114, 182, 0.14);

    --orange: #FB923C;
    --orange-soft: rgba(251, 146, 60, 0.14);

    --yellow: #FACC15;
    --red: #FB7185;

    --panel: rgba(18, 24, 34, 0.92);
    --panel-2: rgba(24, 31, 43, 0.94);

    --text: #F8FAFC;
    --muted: #94A3B8;
}


.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(168, 85, 247, 0.10),
            transparent 23%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(30, 215, 96, 0.10),
            transparent 26%
        ),
        radial-gradient(
            circle at 70% 80%,
            rgba(56, 189, 248, 0.08),
            transparent 26%
        ),
        #0B0F16;
}


.block-container {
    max-width: 1480px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* ==========================================================
   HERO
   ========================================================== */

.bp-hero {
    position: relative;
    overflow: hidden;

    border-radius: 30px;

    padding:
        46px 48px
        44px 48px;

    margin-bottom: 22px;

    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(30, 215, 96, 0.33),
            transparent 29%
        ),
        radial-gradient(
            circle at 12% 95%,
            rgba(168, 85, 247, 0.26),
            transparent 36%
        ),
        linear-gradient(
            130deg,
            #111827 0%,
            #151A24 42%,
            #0F1720 100%
        );

    border:
        1px solid
        rgba(255, 255, 255, 0.09);

    box-shadow:
        0 25px 65px
        rgba(0, 0, 0, 0.30);
}


.bp-orb-1 {
    position: absolute;

    width: 180px;
    height: 180px;

    right: -40px;
    top: -60px;

    border-radius: 50%;

    background:
        rgba(30, 215, 96, 0.14);

    filter: blur(2px);
}


.bp-orb-2 {
    position: absolute;

    width: 140px;
    height: 140px;

    left: 45%;
    bottom: -100px;

    border-radius: 50%;

    background:
        rgba(168, 85, 247, 0.18);
}


.bp-badge {
    display: inline-flex;

    align-items: center;

    gap: 8px;

    border-radius: 999px;

    padding:
        7px 13px;

    margin-bottom: 15px;

    color: #8AF0AB;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 1.2px;

    background:
        rgba(30, 215, 96, 0.10);

    border:
        1px solid
        rgba(30, 215, 96, 0.25);
}


.bp-title {
    position: relative;

    margin: 0;

    font-size: 50px;
    font-weight: 900;

    line-height: 1.02;

    color: #F8FAFC;
}


.bp-title-gradient {
    background:
        linear-gradient(
            90deg,
            #1ED760,
            #52E9A8,
            #38BDF8
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color:
        transparent;
}


.bp-subtitle {
    position: relative;

    max-width: 880px;

    margin:
        17px 0 0 0;

    color: #B4BECC;

    font-size: 16px;
    line-height: 1.75;
}


.bp-stack {
    display: inline-flex;

    gap: 8px;

    flex-wrap: wrap;

    margin-top: 22px;
}


.bp-chip {
    padding:
        7px 11px;

    border-radius: 10px;

    color: #D9E2EC;

    background:
        rgba(255, 255, 255, 0.055);

    border:
        1px solid
        rgba(255, 255, 255, 0.075);

    font-size: 12px;
}


/* ==========================================================
   FEATURE CARDS
   ========================================================== */

.bp-card {
    height: 168px;

    padding: 21px;

    border-radius: 21px;

    border:
        1px solid
        rgba(255, 255, 255, 0.075);

    background:
        linear-gradient(
            145deg,
            rgba(24, 31, 43, 0.96),
            rgba(16, 22, 31, 0.97)
        );

    transition:
        transform .20s ease,
        border-color .20s ease,
        box-shadow .20s ease;
}


.bp-card:hover {
    transform:
        translateY(-4px);

    border-color:
        rgba(255, 255, 255, 0.16);

    box-shadow:
        0 15px 34px
        rgba(0, 0, 0, 0.22);
}


.bp-card-icon {
    width: 44px;
    height: 44px;

    display: flex;

    justify-content: center;
    align-items: center;

    border-radius: 14px;

    font-size: 22px;

    margin-bottom: 13px;
}


.icon-green {
    background: var(--green-soft);
}


.icon-purple {
    background: var(--purple-soft);
}


.icon-blue {
    background: var(--blue-soft);
}


.icon-pink {
    background: var(--pink-soft);
}


.bp-card-title {
    margin-bottom: 6px;

    color: #F8FAFC;

    font-size: 16px;
    font-weight: 800;
}


.bp-card-text {
    color: #96A2B3;

    font-size: 13px;
    line-height: 1.52;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

.bp-side-brand {
    font-size: 24px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #F8FAFC,
            #1ED760
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color:
        transparent;
}


.bp-side-sub {
    color: #8C99A9;

    font-size: 12px;

    margin-top: 2px;
}


.bp-label {
    color: #718096;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.4px;

    text-transform: uppercase;

    margin-bottom: 5px;
}


.bp-online {
    display: inline-flex;

    align-items: center;

    gap: 5px;

    padding:
        6px 10px;

    border-radius: 999px;

    color: #7AE9A0;

    background:
        rgba(30, 215, 96, 0.09);

    border:
        1px solid
        rgba(30, 215, 96, 0.18);

    font-size: 11px;
    font-weight: 700;
}


/* ==========================================================
   SECTION HEADER
   ========================================================== */

.bp-section {
    margin:
        7px 0
        18px 0;
}


.bp-section-kicker {
    color: #5EEA91;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.3px;
}


.bp-section-title {
    margin:
        4px 0 4px 0;

    color: #F8FAFC;

    font-size: 28px;
    font-weight: 850;
}


.bp-section-text {
    color: #8997A9;

    font-size: 13px;
}


/* ==========================================================
   KPI CARDS
   ========================================================== */

.bp-kpi {
    min-height: 126px;

    padding: 19px;

    border-radius: 20px;

    background:
        rgba(19, 26, 37, 0.93);

    border:
        1px solid
        rgba(255, 255, 255, 0.07);

    overflow: hidden;

    position: relative;
}


.bp-kpi::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;

    width: 5px;
    height: 100%;
}


.kpi-blue::before {
    background: #38BDF8;
}


.kpi-green::before {
    background: #1ED760;
}


.kpi-red::before {
    background: #FB7185;
}


.kpi-purple::before {
    background: #A855F7;
}


.bp-kpi-label {
    color: #8896A8;

    font-size: 12px;
    font-weight: 700;
}


.bp-kpi-value {
    margin-top: 8px;

    color: #F8FAFC;

    font-size: 30px;
    font-weight: 900;
}


.bp-kpi-note {
    margin-top: 3px;

    color: #667487;

    font-size: 11px;
}


/* ==========================================================
   REPUTATION HERO
   ========================================================== */

.bp-reputation {
    padding: 22px;

    border-radius: 21px;

    border:
        1px solid
        rgba(255, 255, 255, 0.08);

    background:
        linear-gradient(
            110deg,
            rgba(30, 215, 96, 0.08),
            rgba(56, 189, 248, 0.06),
            rgba(168, 85, 247, 0.08)
        );
}


.bp-rep-label {
    color: #8FA0B3;

    font-size: 12px;
}


.bp-rep-title {
    margin-top: 4px;

    font-size: 23px;
    font-weight: 850;
}


/* ==========================================================
   MANAGER CARDS
   ========================================================== */

.bp-manager {
    padding: 20px;

    border-radius: 19px;

    border:
        1px solid
        rgba(255, 255, 255, 0.075);

    background:
        rgba(19, 26, 37, 0.91);

    margin-bottom: 12px;
}


.bp-manager-top {
    display: flex;

    align-items: center;

    gap: 12px;
}


.bp-avatar {
    min-width: 47px;
    width: 47px;

    height: 47px;

    border-radius: 15px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 23px;
}


.avatar-tech {
    background:
        rgba(56, 189, 248, 0.14);
}


.avatar-product {
    background:
        rgba(168, 85, 247, 0.16);
}


.avatar-service {
    background:
        rgba(30, 215, 96, 0.13);
}


.avatar-marketing {
    background:
        rgba(244, 114, 182, 0.15);
}


.avatar-subscription {
    background:
        rgba(251, 146, 60, 0.15);
}


.bp-manager-title {
    color: #F8FAFC;

    font-size: 17px;

    font-weight: 850;
}


.bp-manager-provider {
    color: #8290A2;

    font-size: 11px;

    margin-top: 2px;
}


.bp-provider {
    display: inline-block;

    margin-top: 10px;

    padding:
        5px 9px;

    border-radius: 8px;

    font-size: 11px;
    font-weight: 700;
}


.provider-gemini {
    color: #CDA8FF;

    background:
        rgba(168, 85, 247, 0.11);
}


.provider-openrouter {
    color: #7DD3FC;

    background:
        rgba(56, 189, 248, 0.10);
}


/* ==========================================================
   EXECUTIVE PANEL
   ========================================================== */

.bp-executive {
    padding: 25px;

    border-radius: 24px;

    background:
        radial-gradient(
            circle at top right,
            rgba(168, 85, 247, 0.18),
            transparent 38%
        ),
        linear-gradient(
            135deg,
            rgba(25, 33, 47, 0.97),
            rgba(15, 21, 30, 0.97)
        );

    border:
        1px solid
        rgba(168, 85, 247, 0.20);
}


/* ==========================================================
   REPORT LABEL
   ========================================================== */

.bp-report-source {
    display: inline-flex;

    gap: 7px;

    align-items: center;

    padding:
        6px 10px;

    border-radius: 8px;

    background:
        rgba(255, 255, 255, 0.05);

    color: #A5B0C0;

    font-size: 11px;
}


/* ==========================================================
   NATIVE STREAMLIT
   ========================================================== */

header[data-testid="stHeader"] {
    background: transparent;
}


[data-testid="stDataFrame"] {
    border-radius: 16px;

    overflow: hidden;
}


[data-testid="stFileUploader"] {
    border-radius: 18px;
}


button[data-baseweb="tab"] {
    font-weight: 700;
}


/* Primary buttons */

div[data-testid="stButton"] > button[kind="primary"] {
    border-radius: 12px;

    font-weight: 750;
}


/* Download buttons */

div[data-testid="stDownloadButton"] > button {
    border-radius: 12px;

    font-weight: 700;
}

</style>
"""
)


# ============================================================
# HELPERS
# ============================================================

def section_header(
    kicker: str,
    title: str,
    text: str,
):
    st.html(
        f"""
<div class="bp-section">
    <div class="bp-section-kicker">
        {kicker}
    </div>

    <div class="bp-section-title">
        {title}
    </div>

    <div class="bp-section-text">
        {text}
    </div>
</div>
"""
    )


def kpi_card(
    label: str,
    value: str,
    note: str,
    css_class: str,
):
    st.html(
        f"""
<div class="bp-kpi {css_class}">
    <div class="bp-kpi-label">
        {label}
    </div>

    <div class="bp-kpi-value">
        {value}
    </div>

    <div class="bp-kpi-note">
        {note}
    </div>
</div>
"""
    )


def manager_visual(
    manager_name: str,
):
    visuals = {
        "Technical Manager": {
            "emoji": "🛠️",
            "avatar": "avatar-tech",
            "short": "Technical reliability & performance",
        },

        "Product Manager": {
            "emoji": "🧩",
            "avatar": "avatar-product",
            "short": "Product features & user experience",
        },

        "Customer Service Manager": {
            "emoji": "🎧",
            "avatar": "avatar-service",
            "short": "Customer complaints & service recovery",
        },

        "Marketing Manager": {
            "emoji": "📣",
            "avatar": "avatar-marketing",
            "short": "Brand perception & communication",
        },

        "Subscription Manager": {
            "emoji": "💳",
            "avatar": "avatar-subscription",
            "short": "Pricing, billing & subscription value",
        },
    }

    return visuals[
        manager_name
    ]


def get_reputation_status(
    score: float,
):
    if score >= 80:
        return (
            "Very Positive",
            "🟢",
            "#1ED760",
        )

    if score >= 60:
        return (
            "Positive",
            "🟢",
            "#52E9A8",
        )

    if score >= 40:
        return (
            "Mixed",
            "🟡",
            "#FACC15",
        )

    if score >= 20:
        return (
            "Negative",
            "🔴",
            "#FB923C",
        )

    return (
        "Very Negative",
        "🔴",
        "#FB7185",
    )


def reset_management_reports():
    st.session_state[
        "manager_reports"
    ] = {}

    st.session_state[
        "executive_report"
    ] = None


# ============================================================
# SESSION STATE
# ============================================================

if (
    "prediction_results"
    not in st.session_state
):
    st.session_state[
        "prediction_results"
    ] = None


if (
    "analysis_summary"
    not in st.session_state
):
    st.session_state[
        "analysis_summary"
    ] = None


if (
    "manager_reports"
    not in st.session_state
):
    st.session_state[
        "manager_reports"
    ] = {}


if (
    "executive_report"
    not in st.session_state
):
    st.session_state[
        "executive_report"
    ] = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
<div class="bp-side-brand">
    🎧 BrandPulse AI
</div>

<div class="bp-side-sub">
    Reputation Intelligence Platform
</div>
"""
    )

    st.divider()


    st.html(
        """
<div class="bp-label">
    PREDICTIVE AI
</div>
"""
    )

    st.markdown(
        "### 🧠 DistilBERT"
    )

    st.caption(
        "Binary Spotify review "
        "sentiment classification"
    )

    st.html(
        """
<span class="bp-online">
    ● Model Online
</span>
"""
    )


    st.divider()


    st.html(
        """
<div class="bp-label">
    GENERATIVE AI
</div>
"""
    )

    st.write(
        "✨ Gemini"
    )

    st.write(
        "🌐 OpenRouter Free"
    )


    st.divider()


    st.html(
        """
<div class="bp-label">
    SENTIMENT CLASSES
</div>
"""
    )

    st.write(
        "🟢 Positive"
    )

    st.write(
        "🔴 Negative"
    )


    st.divider()


    st.html(
        """
<div class="bp-label">
    INTELLIGENCE FLOW
</div>
"""
    )

    st.markdown(
        """
**01** · Upload Reviews

**02** · DistilBERT Prediction

**03** · Reputation Analysis

**04** · Issue Intelligence

**05** · AI Management Council

**06** · Executive Report
"""
    )


    st.divider()


    st.caption(
        "Final Year Project"
    )

    st.caption(
        "Online Review-Based "
        "Brand Reputation Prediction "
        "Using NLP Techniques"
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
<div class="bp-hero">

    <div class="bp-orb-1"></div>
    <div class="bp-orb-2"></div>

    <div class="bp-badge">
        ✦ AI-POWERED BRAND INTELLIGENCE
    </div>

    <div class="bp-title">
        Brand<span class="bp-title-gradient">Pulse AI</span>
    </div>

    <p class="bp-subtitle">
        Turn Spotify customer reviews into decision-ready
        brand intelligence. DistilBERT identifies sentiment,
        analytical modules expose reputation issues, and
        role-based Gemini and OpenRouter managers translate
        the evidence into departmental improvement strategies.
    </p>

    <div class="bp-stack">
        <span class="bp-chip">🧠 DistilBERT</span>
        <span class="bp-chip">✨ Gemini</span>
        <span class="bp-chip">🌐 OpenRouter Free</span>
        <span class="bp-chip">📊 Brand Analytics</span>
        <span class="bp-chip">🤖 Multi-Agent Management</span>
    </div>

</div>
"""
)


# ============================================================
# FEATURE STRIP
# ============================================================

feature_1, feature_2, feature_3, feature_4 = (
    st.columns(
        4,
        gap="medium",
    )
)


with feature_1:
    st.html(
        """
<div class="bp-card">

    <div class="bp-card-icon icon-green">
        🧠
    </div>

    <div class="bp-card-title">
        Predictive Intelligence
    </div>

    <div class="bp-card-text">
        Your trained DistilBERT model classifies
        individual and batch Spotify reviews as
        positive or negative.
    </div>

</div>
"""
    )


with feature_2:
    st.html(
        """
<div class="bp-card">

    <div class="bp-card-icon icon-blue">
        📊
    </div>

    <div class="bp-card-title">
        Reputation Analytics
    </div>

    <div class="bp-card-text">
        Sentiment predictions become brand-level
        indicators, issue distributions and
        customer-voice intelligence.
    </div>

</div>
"""
    )


with feature_3:
    st.html(
        """
<div class="bp-card">

    <div class="bp-card-icon icon-purple">
        🤖
    </div>

    <div class="bp-card-title">
        AI Management Council
    </div>

    <div class="bp-card-text">
        Five department managers analyse the same
        evidence through different organisational
        responsibilities.
    </div>

</div>
"""
    )


with feature_4:
    st.html(
        """
<div class="bp-card">

    <div class="bp-card-icon icon-pink">
        👔
    </div>

    <div class="bp-card-title">
        Executive Intelligence
    </div>

    <div class="bp-card-text">
        Gemini consolidates departmental findings
        into prioritised organisation-wide actions
        and measurable KPIs.
    </div>

</div>
"""
    )


st.write("")


# ============================================================
# MAIN TABS
# ============================================================

(
    single_tab,
    batch_tab,
    dashboard_tab,
    management_tab,
) = st.tabs(
    [
        "🧪 Single Review",
        "📂 Batch Intelligence",
        "📈 Reputation Dashboard",
        "🤖 AI Management Council",
    ]
)


# ============================================================
# TAB 1 — SINGLE REVIEW
# ============================================================

with single_tab:

    section_header(
        "DISTILBERT LAB",
        "Single Review Intelligence",
        (
            "Enter one Spotify review and inspect "
            "the deployed DistilBERT prediction."
        ),
    )


    input_column, output_column = (
        st.columns(
            [1.55, 1],
            gap="large",
        )
    )


    with input_column:

        with st.container(
            border=True,
        ):

            st.markdown(
                "### ✍️ Customer Review"
            )

            review_text = (
                st.text_area(
                    "Review",
                    placeholder=(
                        "Example: The latest Spotify "
                        "update keeps crashing and "
                        "playback stops randomly."
                    ),
                    height=200,
                    label_visibility="collapsed",
                )
            )

            st.caption(
                "Enter an English-language "
                "Spotify customer review."
            )


            analyse_single = (
                st.button(
                    "✨ Analyse Review",
                    type="primary",
                    width="stretch",
                    key="analyse_single",
                )
            )


    with output_column:

        with st.container(
            border=True,
        ):

            st.markdown(
                "### 🎯 AI Prediction"
            )


            if not analyse_single:

                st.info(
                    "Your DistilBERT result "
                    "will appear here."
                )


            elif not review_text.strip():

                st.warning(
                    "Enter a review before "
                    "running the analysis."
                )


            else:

                try:

                    with st.spinner(
                        "DistilBERT is analysing "
                        "the review..."
                    ):

                        result = (
                            predict_sentiment(
                                review_text
                            )
                        )


                    sentiment = (
                        result[
                            "sentiment"
                        ]
                        .strip()
                        .lower()
                    )


                    confidence = (
                        float(
                            result[
                                "confidence"
                            ]
                        )
                        * 100
                    )


                    if (
                        sentiment
                        == "positive"
                    ):

                        st.success(
                            "🟢 Positive Sentiment"
                        )

                        st.write(
                            "The review reflects "
                            "a favourable customer "
                            "experience."
                        )


                    elif (
                        sentiment
                        == "negative"
                    ):

                        st.error(
                            "🔴 Negative Sentiment"
                        )

                        st.write(
                            "The review contains "
                            "customer dissatisfaction "
                            "that may affect brand "
                            "perception."
                        )


                    else:

                        st.info(
                            sentiment.title()
                        )


                    st.metric(
                        "Model Confidence",
                        f"{confidence:.2f}%",
                    )


                    st.progress(
                        max(
                            0.0,
                            min(
                                1.0,
                                confidence / 100,
                            ),
                        ),
                        width="stretch",
                    )


                    st.caption(
                        "Confidence is the model's "
                        "output probability, not a "
                        "guarantee of correctness."
                    )


                except Exception as error:

                    st.error(
                        "The review could not "
                        "be analysed."
                    )

                    st.exception(
                        error
                    )


# ============================================================
# TAB 2 — BATCH INTELLIGENCE
# ============================================================

with batch_tab:

    section_header(
        "BATCH ANALYSIS",
        "Customer Review Intelligence",
        (
            "Upload CSV or XLSX reviews, run "
            "DistilBERT in batches and generate "
            "brand-level analytical evidence."
        ),
    )


    upload_column, guide_column = (
        st.columns(
            [1.55, 1],
            gap="large",
        )
    )


    with upload_column:

        with st.container(
            border=True,
        ):

            st.markdown(
                "### 📂 Upload Review Dataset"
            )

            uploaded_file = (
                st.file_uploader(
                    "Review dataset",
                    type=[
                        "csv",
                        "xlsx",
                    ],
                    label_visibility="collapsed",
                )
            )

            st.caption(
                "Supported formats: CSV and XLSX."
            )


    with guide_column:

        with st.container(
            border=True,
        ):

            st.markdown(
                "### 📌 Expected Format"
            )

            st.write(
                "Your file needs at least "
                "one review-text column."
            )

            st.code(
                "review_text\n"
                "Spotify is easy to use...\n"
                "The app keeps crashing...",
                language=None,
            )


    if uploaded_file is not None:

        try:

            filename = (
                uploaded_file.name
                .lower()
            )


            if filename.endswith(
                ".csv"
            ):

                uploaded_df = (
                    pd.read_csv(
                        uploaded_file
                    )
                )


            else:

                uploaded_df = (
                    pd.read_excel(
                        uploaded_file
                    )
                )


            st.write("")


            dataset_left, dataset_right = (
                st.columns(
                    [3, 1],
                    gap="medium",
                )
            )


            with dataset_left:

                st.markdown(
                    "### Dataset Preview"
                )

                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True,
                )


            with dataset_right:

                st.markdown(
                    "### Dataset"
                )

                st.metric(
                    "Rows",
                    f"{len(uploaded_df):,}",
                )

                st.metric(
                    "Columns",
                    len(
                        uploaded_df.columns
                    ),
                )


            review_column = (
                st.selectbox(
                    (
                        "Select the column "
                        "containing review text"
                    ),
                    options=(
                        uploaded_df
                        .columns
                        .tolist()
                    ),
                )
            )


            valid_reviews = (
                uploaded_df[
                    review_column
                ]
                .dropna()
                .astype(str)
                .str.strip()
            )


            valid_reviews = (
                valid_reviews[
                    valid_reviews.ne("")
                ]
            )


            st.info(
                (
                    f"**{len(valid_reviews):,}** "
                    "valid reviews are ready "
                    "for DistilBERT analysis."
                )
            )


            run_batch = (
                st.button(
                    "🚀 Run Brand Intelligence Analysis",
                    type="primary",
                    width="stretch",
                    key="run_batch",
                )
            )


            if run_batch:

                if (
                    len(valid_reviews)
                    == 0
                ):

                    st.warning(
                        "No valid reviews "
                        "were found."
                    )


                else:

                    try:

                        with st.status(
                            "Launching BrandPulse analysis...",
                            expanded=True,
                        ) as status:

                            st.write(
                                "🧠 DistilBERT is "
                                "classifying reviews..."
                            )


                            prediction_list = (
                                predict_batch(
                                    valid_reviews.tolist(),
                                    batch_size=16,
                                )
                            )


                            prediction_df = (
                                pd.DataFrame(
                                    prediction_list
                                )
                            )


                            st.write(
                                "📊 Calculating "
                                "reputation indicators..."
                            )


                            (
                                analysed_df,
                                summary,
                            ) = (
                                analyse_predictions(
                                    prediction_df
                                )
                            )


                            st.write(
                                "🔎 Mapping negative "
                                "review issue categories..."
                            )


                            st.session_state[
                                "prediction_results"
                            ] = analysed_df


                            st.session_state[
                                "analysis_summary"
                            ] = summary


                            # Important:
                            # New dataset = old reports invalid.
                            reset_management_reports()


                            status.update(
                                label=(
                                    "Brand intelligence "
                                    "analysis completed."
                                ),
                                state="complete",
                                expanded=False,
                            )


                        st.toast(
                            "Brand analysis completed.",
                            icon="✅",
                        )


                    except Exception as error:

                        st.error(
                            "Batch analysis failed."
                        )

                        st.exception(
                            error
                        )


        except Exception as error:

            st.error(
                "The uploaded file could "
                "not be read."
            )

            st.exception(
                error
            )


    # --------------------------------------------------------
    # BATCH RESULTS
    # --------------------------------------------------------

    if (
        st.session_state[
            "prediction_results"
        ]
        is not None
    ):

        st.divider()


        section_header(
            "MODEL OUTPUT",
            "Prediction Intelligence",
            (
                "Review-level DistilBERT "
                "predictions and detected issues."
            ),
        )


        display_results = (
            st.session_state[
                "prediction_results"
            ].copy()
        )


        display_results[
            "confidence"
        ] = (
            display_results[
                "confidence"
            ]
            .astype(float)
            .mul(100)
            .round(2)
        )


        display_results.rename(
            columns={
                "review_text":
                    "Review",

                "predicted_sentiment":
                    "Sentiment",

                "confidence":
                    "Confidence (%)",

                "issues":
                    "Detected Issues",
            },
            inplace=True,
        )


        st.dataframe(
            display_results,
            width="stretch",
            hide_index=True,
            column_config={
                "Confidence (%)":
                    st.column_config.ProgressColumn(
                        "Confidence (%)",
                        min_value=0,
                        max_value=100,
                        format="%.2f%%",
                    ),
            },
        )


        export_csv = (
            display_results
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            "⬇️ Download Prediction Results",
            data=export_csv,
            file_name=(
                "brandpulse_prediction_results.csv"
            ),
            mime="text/csv",
            width="stretch",
        )


# ============================================================
# TAB 3 — REPUTATION DASHBOARD
# ============================================================

with dashboard_tab:

    section_header(
        "REPUTATION INTELLIGENCE",
        "Brand Reputation Dashboard",
        (
            "Explore aggregated sentiment, "
            "customer issues and review-language "
            "patterns generated from the current dataset."
        ),
    )


    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )


    if summary is None:

        with st.container(
            border=True,
        ):

            st.info(
                "Run **Batch Intelligence** first "
                "to generate this dashboard."
            )


    else:

        score = float(
            summary[
                "reputation_score"
            ]
        )


        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        kpi_1, kpi_2, kpi_3, kpi_4 = (
            st.columns(
                4,
                gap="medium",
            )
        )


        with kpi_1:

            kpi_card(
                "REVIEWS ANALYSED",
                f"{summary['total_reviews']:,}",
                "Current analysis dataset",
                "kpi-blue",
            )


        with kpi_2:

            kpi_card(
                "POSITIVE REVIEWS",
                f"{summary['positive_reviews']:,}",
                (
                    f"{summary['positive_percentage']}"
                    "% of classified reviews"
                ),
                "kpi-green",
            )


        with kpi_3:

            kpi_card(
                "NEGATIVE REVIEWS",
                f"{summary['negative_reviews']:,}",
                (
                    f"{summary['negative_percentage']}"
                    "% of classified reviews"
                ),
                "kpi-red",
            )


        with kpi_4:

            kpi_card(
                "REPUTATION SCORE",
                f"{score:.2f}%",
                "Project-defined indicator",
                "kpi-purple",
            )


        st.write("")


        # ----------------------------------------------------
        # REPUTATION STATUS
        # ----------------------------------------------------

        (
            reputation_name,
            reputation_emoji,
            reputation_color,
        ) = get_reputation_status(
            score
        )


        st.html(
            f"""
<div class="bp-reputation">

    <div class="bp-rep-label">
        CURRENT BRAND REPUTATION
    </div>

    <div
        class="bp-rep-title"
        style="color:{reputation_color};"
    >
        {reputation_emoji}
        {reputation_name}
    </div>

</div>
"""
        )


        st.progress(
            max(
                0.0,
                min(
                    1.0,
                    score / 100,
                ),
            ),
            width="stretch",
        )


        st.write("")


        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        sentiment_column, issue_column = (
            st.columns(
                2,
                gap="large",
            )
        )


        with sentiment_column:

            with st.container(
                border=True,
            ):

                st.markdown(
                    "### 🎯 Sentiment Distribution"
                )


                sentiment_df = (
                    pd.DataFrame(
                        {
                            "Sentiment": [
                                "Positive",
                                "Negative",
                            ],

                            "Reviews": [
                                summary[
                                    "positive_reviews"
                                ],

                                summary[
                                    "negative_reviews"
                                ],
                            ],
                        }
                    )
                )


                sentiment_chart = (
                    px.pie(
                        sentiment_df,
                        names="Sentiment",
                        values="Reviews",
                        hole=0.67,
                        color="Sentiment",
                        color_discrete_map={
                            "Positive":
                                "#1ED760",

                            "Negative":
                                "#FB7185",
                        },
                    )
                )


                sentiment_chart.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>Reviews: %{value}"
                        "<br>Share: %{percent}"
                        "<extra></extra>"
                    ),
                )


                sentiment_chart.update_layout(
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10,
                    ),

                    legend_title_text="",

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",
                )


                st.plotly_chart(
                    sentiment_chart,
                    width="stretch",
                )


        with issue_column:

            with st.container(
                border=True,
            ):

                st.markdown(
                    "### 🔎 Negative Review Issues"
                )


                issue_counts = (
                    summary[
                        "issue_counts"
                    ]
                )


                if issue_counts:

                    issue_df = (
                        pd.DataFrame(
                            [
                                {
                                    "Issue":
                                        issue,

                                    "Mentions":
                                        count,
                                }

                                for (
                                    issue,
                                    count,
                                )
                                in issue_counts.items()
                            ]
                        )
                    )


                    issue_df = (
                        issue_df
                        .sort_values(
                            "Mentions",
                            ascending=True,
                        )
                    )


                    issue_chart = (
                        px.bar(
                            issue_df,
                            x="Mentions",
                            y="Issue",
                            orientation="h",
                            color="Mentions",
                            color_continuous_scale=[
                                "#38BDF8",
                                "#A855F7",
                                "#F472B6",
                            ],
                        )
                    )


                    issue_chart.update_layout(
                        coloraxis_showscale=False,

                        margin=dict(
                            l=10,
                            r=10,
                            t=10,
                            b=10,
                        ),

                        paper_bgcolor="rgba(0,0,0,0)",

                        plot_bgcolor="rgba(0,0,0,0)",
                    )


                    st.plotly_chart(
                        issue_chart,
                        width="stretch",
                    )


                else:

                    st.success(
                        "No negative issue "
                        "categories were detected."
                    )


        # ----------------------------------------------------
        # CUSTOMER VOICE
        # ----------------------------------------------------

        st.write("")


        section_header(
            "VOICE OF CUSTOMER",
            "Customer Language Intelligence",
            (
                "Frequently occurring terms "
                "within positive and negative "
                "predicted reviews."
            ),
        )


        positive_column, negative_column = (
            st.columns(
                2,
                gap="large",
            )
        )


        with positive_column:

            with st.container(
                border=True,
            ):

                st.markdown(
                    "### 💚 Positive Customer Voice"
                )


                positive_words = (
                    pd.DataFrame(
                        summary[
                            "top_positive_words"
                        ]
                    )
                )


                if (
                    not positive_words.empty
                ):

                    positive_words.rename(
                        columns={
                            "word":
                                "Word",

                            "count":
                                "Frequency",
                        },
                        inplace=True,
                    )


                    st.dataframe(
                        positive_words,
                        width="stretch",
                        hide_index=True,
                    )


                else:

                    st.info(
                        "No positive-word "
                        "data available."
                    )


        with negative_column:

            with st.container(
                border=True,
            ):

                st.markdown(
                    "### 💗 Negative Customer Voice"
                )


                negative_words = (
                    pd.DataFrame(
                        summary[
                            "top_negative_words"
                        ]
                    )
                )


                if (
                    not negative_words.empty
                ):

                    negative_words.rename(
                        columns={
                            "word":
                                "Word",

                            "count":
                                "Frequency",
                        },
                        inplace=True,
                    )


                    st.dataframe(
                        negative_words,
                        width="stretch",
                        hide_index=True,
                    )


                else:

                    st.info(
                        "No negative-word "
                        "data available."
                    )


        # ----------------------------------------------------
        # REVIEWS REQUIRING ATTENTION
        # ----------------------------------------------------

        st.write("")


        section_header(
            "CUSTOMER ATTENTION",
            "Reviews Requiring Attention",
            (
                "Representative negative reviews "
                "that can help management understand "
                "the issues behind the aggregate metrics."
            ),
        )


        negative_samples = (
            summary[
                "sample_negative_reviews"
            ]
        )


        if negative_samples:

            for (
                review_number,
                review,
            ) in enumerate(
                negative_samples,
                start=1,
            ):

                with st.expander(
                    (
                        "🚨 Negative Review "
                        f"{review_number}"
                    )
                ):

                    st.write(
                        review
                    )


        else:

            st.success(
                "No negative reviews "
                "were detected."
            )


        st.info(
            "The Brand Reputation Score is a "
            "project-defined indicator calculated "
            "from the proportion of positive "
            "DistilBERT predictions. It is not "
            "presented as a universal industry "
            "brand-reputation metric."
        )


# ============================================================
# TAB 4 — AI MANAGEMENT COUNCIL
# ============================================================

with management_tab:

    section_header(
        "GENERATIVE AI",
        "AI Management Council",
        (
            "Five role-based managers interpret "
            "the structured brand-reputation "
            "evidence from different departmental "
            "perspectives."
        ),
    )


    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )


    if summary is None:

        with st.container(
            border=True,
        ):

            st.warning(
                "Run **Batch Intelligence** first. "
                "The managers require structured "
                "brand-reputation evidence."
            )


    else:

        # ----------------------------------------------------
        # MANAGEMENT ARCHITECTURE
        # ----------------------------------------------------

        with st.container(
            border=True,
        ):

            architecture_left, architecture_right = (
                st.columns(
                    [1.45, 1],
                    gap="large",
                )
            )


            with architecture_left:

                st.markdown(
                    "### 🏢 Council Architecture"
                )

                st.write(
                    "The managers receive the same "
                    "analysis summary, but each role "
                    "is instructed to focus on its "
                    "own organisational responsibilities."
                )


            with architecture_right:

                architecture_df = (
                    pd.DataFrame(
                        [
                            {
                                "Manager":
                                    manager,

                                "Provider":
                                    (
                                        "Gemini"
                                        if provider
                                        == "gemini"
                                        else
                                        "OpenRouter Free"
                                    ),
                            }

                            for (
                                manager,
                                provider,
                            )
                            in MANAGER_PROVIDERS.items()
                        ]
                    )
                )


                st.dataframe(
                    architecture_df,
                    width="stretch",
                    hide_index=True,
                )


        # ----------------------------------------------------
        # COUNCIL PROGRESS
        # ----------------------------------------------------

        completed_count = len(
            st.session_state[
                "manager_reports"
            ]
        )


        total_managers = len(
            MANAGER_ROLES
        )


        completion_ratio = (
            completed_count
            / total_managers
        )


        st.write("")


        progress_left, progress_right = (
            st.columns(
                [3, 1],
                gap="medium",
            )
        )


        with progress_left:

            st.markdown(
                "### 📋 Council Progress"
            )

            st.progress(
                completion_ratio,
                width="stretch",
            )

            st.caption(
                (
                    f"{completed_count} of "
                    f"{total_managers} department "
                    "reports generated."
                )
            )


        with progress_right:

            kpi_card(
                "REPORTS READY",
                (
                    f"{completed_count}"
                    f"/{total_managers}"
                ),
                "AI Council completion",
                "kpi-purple",
            )


        st.write("")


        # ----------------------------------------------------
        # MANAGER TABS
        # ----------------------------------------------------

        (
            technical_tab,
            product_tab,
            service_tab,
            marketing_tab,
            subscription_tab,
        ) = st.tabs(
            [
                "🛠 Technical",
                "🧩 Product",
                "🎧 Customer Service",
                "📣 Marketing",
                "💳 Subscription",
            ]
        )


        manager_tab_map = {
            "Technical Manager":
                technical_tab,

            "Product Manager":
                product_tab,

            "Customer Service Manager":
                service_tab,

            "Marketing Manager":
                marketing_tab,

            "Subscription Manager":
                subscription_tab,
        }


        # ----------------------------------------------------
        # EACH MANAGER
        # ----------------------------------------------------

        for (
            manager_name,
            manager_tab,
        ) in manager_tab_map.items():

            with manager_tab:

                visual = (
                    manager_visual(
                        manager_name
                    )
                )


                provider_key = (
                    MANAGER_PROVIDERS[
                        manager_name
                    ]
                )


                if (
                    provider_key
                    == "gemini"
                ):

                    provider_name = (
                        "Gemini"
                    )

                    provider_css = (
                        "provider-gemini"
                    )

                    provider_emoji = (
                        "✨"
                    )


                else:

                    provider_name = (
                        "OpenRouter Free"
                    )

                    provider_css = (
                        "provider-openrouter"
                    )

                    provider_emoji = (
                        "🌐"
                    )


                st.html(
                    f"""
<div class="bp-manager">

    <div class="bp-manager-top">

        <div
            class="bp-avatar
                   {visual['avatar']}"
        >
            {visual['emoji']}
        </div>

        <div>

            <div class="bp-manager-title">
                {manager_name}
            </div>

            <div class="bp-manager-provider">
                {visual['short']}
            </div>

        </div>

    </div>

    <span
        class="bp-provider
               {provider_css}"
    >
        {provider_emoji}
        {provider_name}
    </span>

</div>
"""
                )


                with st.expander(
                    "View department responsibility"
                ):

                    st.write(
                        MANAGER_ROLES[
                            manager_name
                        ]
                    )


                button_key = (
                    "generate_"
                    + manager_name
                    .lower()
                    .replace(
                        " ",
                        "_"
                    )
                )


                if st.button(
                    (
                        "✨ Generate "
                        f"{manager_name} Report"
                    ),
                    type="primary",
                    width="stretch",
                    key=button_key,
                ):

                    try:

                        with st.status(
                            (
                                f"{manager_name} "
                                "is analysing the evidence..."
                            ),
                            expanded=True,
                        ) as status:

                            st.write(
                                "📊 Reading reputation "
                                "statistics..."
                            )

                            st.write(
                                "🔎 Reviewing relevant "
                                "customer issues..."
                            )

                            st.write(
                                "🧠 Interpreting findings "
                                "from the department "
                                "perspective..."
                            )

                            st.write(
                                "💡 Building actionable "
                                "recommendations..."
                            )


                            report = (
                                generate_manager_report(
                                    manager_name,
                                    summary,
                                )
                            )


                            st.session_state[
                                "manager_reports"
                            ][
                                manager_name
                            ] = report


                            # Existing executive report
                            # becomes outdated when any
                            # department report changes.
                            st.session_state[
                                "executive_report"
                            ] = None


                            status.update(
                                label=(
                                    f"{manager_name} "
                                    "report completed."
                                ),
                                state="complete",
                                expanded=False,
                            )


                        st.toast(
                            (
                                f"{manager_name} "
                                "report generated."
                            ),
                            icon="✅",
                        )


                    except Exception as error:

                        st.error(
                            (
                                f"{manager_name} "
                                "report generation failed."
                            )
                        )

                        st.exception(
                            error
                        )


                # --------------------------------------------
                # DISPLAY REPORT
                # --------------------------------------------

                manager_report = (
                    st.session_state[
                        "manager_reports"
                    ].get(
                        manager_name
                    )
                )


                if manager_report:

                    st.write("")


                    with st.container(
                        border=True,
                    ):

                        report_provider = (
                            manager_report.get(
                                "provider",
                                "Unknown",
                            )
                        )


                        report_model = (
                            manager_report.get(
                                "model",
                                "Unknown",
                            )
                        )


                        st.html(
                            f"""
<div class="bp-report-source">
    🤖 Provider: {report_provider}
    &nbsp;&nbsp;•&nbsp;&nbsp;
    Model: {report_model}
</div>
"""
                        )


                        st.write("")


                        st.markdown(
                            manager_report[
                                "content"
                            ]
                        )


                    report_text = (
                        manager_report[
                            "content"
                        ]
                    )


                    st.download_button(
                        (
                            "⬇️ Download "
                            f"{manager_name} Report"
                        ),
                        data=report_text,
                        file_name=(
                            manager_name
                            .lower()
                            .replace(
                                " ",
                                "_"
                            )
                            + "_report.md"
                        ),
                        mime="text/markdown",
                        width="stretch",
                        key=(
                            "download_"
                            + manager_name
                            .lower()
                            .replace(
                                " ",
                                "_"
                            )
                        ),
                    )


                    if (
                        report_provider
                        == "OpenRouter"
                    ):

                        st.caption(
                            "OpenRouter was requested "
                            "through `openrouter/free`. "
                            "The actual free model used "
                            "for this report is shown "
                            "above."
                        )


        # ----------------------------------------------------
        # EXECUTIVE MANAGER
        # ----------------------------------------------------

        st.divider()


        st.html(
            """
<div class="bp-executive">

    <div class="bp-badge">
        👔 EXECUTIVE INTELLIGENCE
    </div>

    <div
        style="
            font-size:28px;
            font-weight:900;
            color:#F8FAFC;
        "
    >
        Executive Manager
    </div>

    <div
        style="
            margin-top:8px;
            color:#97A5B7;
            line-height:1.6;
            font-size:13px;
        "
    >
        Gemini consolidates all five
        department reports into a single,
        prioritised organisation-wide
        brand improvement strategy.
    </div>

</div>
"""
        )


        reports = (
            st.session_state[
                "manager_reports"
            ]
        )


        reports_ready = len(
            reports
        )


        st.write("")


        readiness_left, readiness_right = (
            st.columns(
                [2, 1],
                gap="medium",
            )
        )


        with readiness_left:

            if (
                reports_ready
                == total_managers
            ):

                st.success(
                    "✅ All department reports "
                    "are ready for executive "
                    "consolidation."
                )


            else:

                missing_managers = (
                    [
                        manager

                        for manager
                        in MANAGER_ROLES

                        if manager
                        not in reports
                    ]
                )


                st.info(
                    (
                        f"Generate the remaining "
                        f"**{len(missing_managers)}** "
                        "department report(s) first."
                    )
                )


                with st.expander(
                    "Reports still required"
                ):

                    for manager in (
                        missing_managers
                    ):

                        st.write(
                            f"• {manager}"
                        )


        with readiness_right:

            kpi_card(
                "EXECUTIVE READY",
                (
                    "YES"
                    if reports_ready
                    == total_managers
                    else "NOT YET"
                ),
                (
                    f"{reports_ready}/"
                    f"{total_managers} reports"
                ),
                (
                    "kpi-green"
                    if reports_ready
                    == total_managers
                    else "kpi-purple"
                ),
            )


        if (
            reports_ready
            == total_managers
        ):

            generate_executive = (
                st.button(
                    "👔 Generate Executive Brand Reputation Report",
                    type="primary",
                    width="stretch",
                    key="generate_executive",
                )
            )


            if generate_executive:

                try:

                    with st.status(
                        (
                            "Executive Manager "
                            "is consolidating "
                            "department intelligence..."
                        ),
                        expanded=True,
                    ) as status:

                        st.write(
                            "📚 Reading all five "
                            "department reports..."
                        )

                        st.write(
                            "🔗 Identifying repeated "
                            "and cross-department issues..."
                        )

                        st.write(
                            "🎯 Ranking immediate and "
                            "long-term priorities..."
                        )

                        st.write(
                            "📏 Consolidating measurable "
                            "management KPIs..."
                        )

                        st.write(
                            "📝 Preparing final "
                            "executive strategy..."
                        )


                        executive_report = (
                            generate_executive_report(
                                summary,
                                reports,
                            )
                        )


                        st.session_state[
                            "executive_report"
                        ] = executive_report


                        status.update(
                            label=(
                                "Executive Brand "
                                "Reputation Report "
                                "completed."
                            ),
                            state="complete",
                            expanded=False,
                        )


                    st.toast(
                        "Executive report generated.",
                        icon="👔",
                    )


                except Exception as error:

                    st.error(
                        "Executive report "
                        "generation failed."
                    )

                    st.exception(
                        error
                    )


        # ----------------------------------------------------
        # EXECUTIVE REPORT
        # ----------------------------------------------------

        executive_report = (
            st.session_state[
                "executive_report"
            ]
        )


        if executive_report:

            st.write("")


            section_header(
                "FINAL MANAGEMENT OUTPUT",
                "Executive Brand Reputation Report",
                (
                    "Organisation-wide synthesis "
                    "of predictive analysis and "
                    "department-level AI intelligence."
                ),
            )


            with st.container(
                border=True,
            ):

                executive_provider = (
                    executive_report.get(
                        "provider",
                        "Gemini",
                    )
                )


                executive_model = (
                    executive_report.get(
                        "model",
                        "Unknown",
                    )
                )


                st.html(
                    f"""
<div class="bp-report-source">
    👔 Executive Provider:
    {executive_provider}

    &nbsp;&nbsp;•&nbsp;&nbsp;

    Model:
    {executive_model}
</div>
"""
                )


                st.write("")


                st.markdown(
                    executive_report[
                        "content"
                    ]
                )


            download_left, download_right = (
                st.columns(
                    2,
                    gap="medium",
                )
            )


            with download_left:

                st.download_button(
                    "⬇️ Download Executive Report",
                    data=(
                        executive_report[
                            "content"
                        ]
                    ),
                    file_name=(
                        "executive_brand_"
                        "reputation_report.md"
                    ),
                    mime="text/markdown",
                    width="stretch",
                )


            with download_right:

                complete_package = {
                    "analysis_summary":
                        summary,

                    "department_reports":
                        reports,

                    "executive_report":
                        executive_report,
                }


                complete_json = json.dumps(
                    complete_package,
                    indent=2,
                    ensure_ascii=False,
                )


                st.download_button(
                    "📦 Download Complete AI Analysis",
                    data=complete_json,
                    file_name=(
                        "brandpulse_complete_"
                        "analysis.json"
                    ),
                    mime="application/json",
                    width="stretch",
                )
