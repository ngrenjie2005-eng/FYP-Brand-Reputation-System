# ============================================================
# BRANDPULSE AI
# Spotify Brand Reputation Intelligence System
# ============================================================

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import analyse_predictions

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
    --blue: #38BDF8;
    --purple: #A855F7;
    --pink: #F472B6;
    --orange: #FB923C;
    --yellow: #FACC15;
    --red: #FB7185;

    --background: #0B0F16;
    --panel: #121923;
    --panel-light: #182231;

    --text-main: #F8FAFC;
    --text-soft: #AAB6C5;
    --text-muted: #748196;
}


/* ==========================================================
   MAIN APPLICATION
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(168, 85, 247, 0.09),
            transparent 22%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(30, 215, 96, 0.09),
            transparent 25%
        ),
        radial-gradient(
            circle at 70% 85%,
            rgba(56, 189, 248, 0.06),
            transparent 25%
        ),
        var(--background);
}


.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* ==========================================================
   HERO
   ========================================================== */

.bp-hero {
    position: relative;

    overflow: hidden;

    padding: 46px 48px;

    margin-bottom: 25px;

    border-radius: 30px;

    background:
        radial-gradient(
            circle at 86% 15%,
            rgba(30, 215, 96, 0.32),
            transparent 29%
        ),
        radial-gradient(
            circle at 12% 100%,
            rgba(168, 85, 247, 0.24),
            transparent 37%
        ),
        linear-gradient(
            130deg,
            #111827 0%,
            #151A24 44%,
            #101923 100%
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.09
        );

    box-shadow:
        0 25px 60px rgba(
            0,
            0,
            0,
            0.30
        );
}


.bp-orb-one {
    position: absolute;

    right: -50px;
    top: -65px;

    width: 190px;
    height: 190px;

    border-radius: 50%;

    background:
        rgba(30, 215, 96, 0.13);
}


.bp-orb-two {
    position: absolute;

    bottom: -110px;
    left: 42%;

    width: 165px;
    height: 165px;

    border-radius: 50%;

    background:
        rgba(168, 85, 247, 0.15);
}


.bp-badge {
    display: inline-flex;

    align-items: center;

    gap: 7px;

    padding: 7px 13px;

    margin-bottom: 16px;

    border-radius: 999px;

    background:
        rgba(30, 215, 96, 0.10);

    border:
        1px solid rgba(
            30,
            215,
            96,
            0.24
        );

    color: #8AF0AB;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1.1px;
}


.bp-title {
    position: relative;

    margin: 0;

    color: #F8FAFC;

    font-size: clamp(
        38px,
        4vw,
        54px
    );

    font-weight: 900;

    line-height: 1.05;
}


.bp-gradient-text {
    background:
        linear-gradient(
            90deg,
            #1ED760,
            #4ADE80,
            #38BDF8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.bp-subtitle {
    position: relative;

    max-width: 900px;

    margin-top: 17px;

    color: #B3BECC;

    font-size: 16px;

    line-height: 1.75;
}


.bp-tech-stack {
    position: relative;

    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin-top: 22px;
}


.bp-chip {
    padding: 7px 11px;

    border-radius: 10px;

    background:
        rgba(
            255,
            255,
            255,
            0.055
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.075
        );

    color: #D9E2EC;

    font-size: 12px;

    white-space: nowrap;
}


/* ==========================================================
   FEATURE CARDS
   ========================================================== */

/*
IMPORTANT FIX:
There is NO fixed height anymore.

The previous version used height:168px,
which caused your text to leave the card.
*/

.bp-feature-card {
    box-sizing: border-box;

    width: 100%;

    min-height: 220px;

    height: auto;

    padding: 23px;

    margin-bottom: 10px;

    border-radius: 22px;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            rgba(24, 33, 45, 0.98),
            rgba(16, 23, 32, 0.98)
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.075
        );

    transition:
        transform 0.20s ease,
        border-color 0.20s ease,
        box-shadow 0.20s ease;
}


.bp-feature-card:hover {
    transform:
        translateY(-4px);

    border-color:
        rgba(
            30,
            215,
            96,
            0.35
        );

    box-shadow:
        0 16px 35px rgba(
            0,
            0,
            0,
            0.23
        );
}


.bp-feature-icon {
    display: flex;

    align-items: center;
    justify-content: center;

    width: 46px;
    height: 46px;

    margin-bottom: 15px;

    border-radius: 15px;

    font-size: 23px;
}


.feature-green {
    background:
        rgba(
            30,
            215,
            96,
            0.14
        );
}


.feature-blue {
    background:
        rgba(
            56,
            189,
            248,
            0.15
        );
}


.feature-purple {
    background:
        rgba(
            168,
            85,
            247,
            0.17
        );
}


.feature-pink {
    background:
        rgba(
            244,
            114,
            182,
            0.16
        );
}


.bp-feature-title {
    margin-bottom: 9px;

    color: #F8FAFC;

    font-size: 16px;

    font-weight: 800;

    line-height: 1.3;

    overflow-wrap: break-word;

    word-break: normal;
}


.bp-feature-text {
    margin: 0;

    color: #9FAABC;

    font-size: 13px;

    line-height: 1.62;

    overflow-wrap: break-word;

    word-wrap: break-word;

    word-break: normal;

    white-space: normal;
}


/* ==========================================================
   RESPONSIVE FEATURE CARDS
   ========================================================== */

@media (
    max-width: 1200px
) {

    .bp-feature-card {
        min-height: 240px;
    }

    .bp-feature-text {
        font-size: 12.5px;
    }
}


@media (
    max-width: 800px
) {

    .bp-hero {
        padding: 30px 25px;
    }

    .bp-feature-card {
        min-height: 190px;
    }

    .bp-title {
        font-size: 38px;
    }
}


/* ==========================================================
   SECTION HEADERS
   ========================================================== */

.bp-section {
    margin:
        7px 0 19px 0;
}


.bp-section-kicker {
    color: #5EEA91;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.35px;
}


.bp-section-title {
    margin:
        4px 0 4px 0;

    color: #F8FAFC;

    font-size: 28px;

    font-weight: 850;
}


.bp-section-text {
    color: #8E9BAD;

    font-size: 13px;

    line-height: 1.5;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

.bp-sidebar-brand {
    font-size: 24px;

    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #F8FAFC,
            #1ED760
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.bp-sidebar-subtitle {
    margin-top: 3px;

    color: #8491A3;

    font-size: 12px;
}


.bp-small-label {
    margin-bottom: 6px;

    color: #6F7D90;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.35px;

    text-transform: uppercase;
}


.bp-online {
    display: inline-flex;

    align-items: center;

    padding: 6px 10px;

    border-radius: 999px;

    color: #7AE9A0;

    background:
        rgba(
            30,
            215,
            96,
            0.09
        );

    border:
        1px solid rgba(
            30,
            215,
            96,
            0.18
        );

    font-size: 11px;

    font-weight: 700;
}


/* ==========================================================
   KPI CARDS
   ========================================================== */

.bp-kpi {
    position: relative;

    overflow: hidden;

    min-height: 126px;

    padding: 20px 20px 20px 24px;

    border-radius: 20px;

    background:
        rgba(
            19,
            26,
            37,
            0.94
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.07
        );
}


.bp-kpi::before {
    position: absolute;

    content: "";

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
    color: #8795A8;

    font-size: 11px;

    font-weight: 750;
}


.bp-kpi-value {
    margin-top: 9px;

    color: #F8FAFC;

    font-size: 30px;

    font-weight: 900;
}


.bp-kpi-note {
    margin-top: 4px;

    color: #68778A;

    font-size: 11px;
}


/* ==========================================================
   REPUTATION STATUS
   ========================================================== */

.bp-reputation-panel {
    padding: 23px;

    border-radius: 22px;

    background:
        linear-gradient(
            110deg,
            rgba(30, 215, 96, 0.07),
            rgba(56, 189, 248, 0.06),
            rgba(168, 85, 247, 0.08)
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.08
        );
}


.bp-reputation-label {
    color: #8796A9;

    font-size: 11px;

    font-weight: 750;
}


.bp-reputation-title {
    margin-top: 6px;

    font-size: 24px;

    font-weight: 900;
}


/* ==========================================================
   MANAGER PROFILE
   ========================================================== */

.bp-manager-profile {
    width: 100%;

    box-sizing: border-box;

    padding: 21px;

    margin-bottom: 14px;

    border-radius: 21px;

    overflow: hidden;

    background:
        rgba(
            19,
            27,
            38,
            0.95
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.075
        );
}


.bp-manager-top {
    display: flex;

    align-items: center;

    gap: 13px;
}


.bp-avatar {
    display: flex;

    flex-shrink: 0;

    align-items: center;
    justify-content: center;

    width: 49px;
    height: 49px;

    border-radius: 16px;

    font-size: 23px;
}


.avatar-tech {
    background:
        rgba(
            56,
            189,
            248,
            0.14
        );
}


.avatar-product {
    background:
        rgba(
            168,
            85,
            247,
            0.16
        );
}


.avatar-service {
    background:
        rgba(
            30,
            215,
            96,
            0.13
        );
}


.avatar-marketing {
    background:
        rgba(
            244,
            114,
            182,
            0.15
        );
}


.avatar-subscription {
    background:
        rgba(
            251,
            146,
            60,
            0.15
        );
}


.bp-manager-name {
    color: #F8FAFC;

    font-size: 18px;

    font-weight: 850;
}


.bp-manager-short {
    margin-top: 2px;

    color: #8492A5;

    font-size: 12px;

    overflow-wrap: break-word;
}


.bp-provider {
    display: inline-block;

    margin-top: 12px;

    padding: 5px 9px;

    border-radius: 9px;

    font-size: 11px;

    font-weight: 750;
}


.provider-gemini {
    color: #CEA9FF;

    background:
        rgba(
            168,
            85,
            247,
            0.12
        );
}


.provider-openrouter {
    color: #7DD3FC;

    background:
        rgba(
            56,
            189,
            248,
            0.11
        );
}


/* ==========================================================
   EXECUTIVE
   ========================================================== */

.bp-executive {
    padding: 27px;

    border-radius: 25px;

    overflow: hidden;

    background:
        radial-gradient(
            circle at top right,
            rgba(168, 85, 247, 0.19),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            rgba(25, 33, 47, 0.98),
            rgba(15, 21, 30, 0.98)
        );

    border:
        1px solid rgba(
            168,
            85,
            247,
            0.21
        );
}


.bp-report-source {
    display: inline-flex;

    flex-wrap: wrap;

    align-items: center;

    gap: 6px;

    padding: 6px 10px;

    border-radius: 9px;

    background:
        rgba(
            255,
            255,
            255,
            0.05
        );

    color: #A8B2C1;

    font-size: 11px;

    overflow-wrap: anywhere;
}


/* ==========================================================
   STREAMLIT COMPONENTS
   ========================================================== */

header[data-testid="stHeader"] {
    background: transparent;
}


button[data-baseweb="tab"] {
    font-weight: 700;
}


[data-testid="stDataFrame"] {
    overflow: hidden;

    border-radius: 16px;
}


div[data-testid="stButton"]
> button[kind="primary"] {
    border-radius: 12px;

    font-weight: 750;
}


div[data-testid="stDownloadButton"]
> button {
    border-radius: 12px;

    font-weight: 700;
}

</style>
"""
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def section_header(
    kicker,
    title,
    text,
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
    label,
    value,
    note,
    css_class,
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


def get_reputation_status(
    score,
):

    if score >= 80:
        return (
            "Very Positive Brand Reputation",
            "🟢",
            "#1ED760",
        )

    if score >= 60:
        return (
            "Positive Brand Reputation",
            "🟢",
            "#52E9A8",
        )

    if score >= 40:
        return (
            "Mixed Brand Reputation",
            "🟡",
            "#FACC15",
        )

    if score >= 20:
        return (
            "Negative Brand Reputation",
            "🔴",
            "#FB923C",
        )

    return (
        "Very Negative Brand Reputation",
        "🔴",
        "#FB7185",
    )


def get_manager_visual(
    manager_name,
):

    manager_styles = {

        "Technical Manager": {
            "emoji": "🛠️",
            "avatar": "avatar-tech",
            "short":
                "Technical reliability, stability and performance",
        },

        "Product Manager": {
            "emoji": "🧩",
            "avatar": "avatar-product",
            "short":
                "Product experience, features and usability",
        },

        "Customer Service Manager": {
            "emoji": "🎧",
            "avatar": "avatar-service",
            "short":
                "Customer complaints, satisfaction and recovery",
        },

        "Marketing Manager": {
            "emoji": "📣",
            "avatar": "avatar-marketing",
            "short":
                "Brand perception, communication and positioning",
        },

        "Subscription Manager": {
            "emoji": "💳",
            "avatar": "avatar-subscription",
            "short":
                "Pricing, Premium, billing and customer value",
        },
    }

    return manager_styles[
        manager_name
    ]


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
<div class="bp-sidebar-brand">
    🎧 BrandPulse AI
</div>

<div class="bp-sidebar-subtitle">
    Brand Reputation Intelligence Platform
</div>
"""
    )


    st.divider()


    st.html(
        """
<div class="bp-small-label">
    PREDICTIVE AI
</div>
"""
    )


    st.markdown(
        "### 🧠 DistilBERT"
    )


    st.caption(
        "Binary sentiment classification "
        "for Spotify customer reviews."
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
<div class="bp-small-label">
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
<div class="bp-small-label">
    CLASSIFICATION
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
<div class="bp-small-label">
    INTELLIGENCE FLOW
</div>
"""
    )


    st.markdown(
        """
**01** · Upload Reviews

**02** · DistilBERT Prediction

**03** · Reputation Analytics

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
        "Online Review-Based Brand Reputation "
        "Prediction Using NLP Techniques"
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
<div class="bp-hero">

    <div class="bp-orb-one"></div>

    <div class="bp-orb-two"></div>

    <div class="bp-badge">
        ✦ AI-POWERED BRAND INTELLIGENCE
    </div>

    <div class="bp-title">

        Brand<span class="bp-gradient-text">Pulse AI</span>

    </div>

    <p class="bp-subtitle">

        Turn Spotify customer reviews into
        decision-ready brand intelligence.
        DistilBERT identifies sentiment,
        analytical modules reveal reputation
        issues, and role-based Gemini and
        OpenRouter managers transform the
        evidence into departmental improvement
        strategies.

    </p>

    <div class="bp-tech-stack">

        <span class="bp-chip">
            🧠 DistilBERT
        </span>

        <span class="bp-chip">
            ✨ Gemini
        </span>

        <span class="bp-chip">
            🌐 OpenRouter Free
        </span>

        <span class="bp-chip">
            📊 Reputation Analytics
        </span>

        <span class="bp-chip">
            🤖 Management Council
        </span>

    </div>

</div>
"""
)


# ============================================================
# FEATURE CARDS
# ============================================================

feature_one, feature_two, feature_three, feature_four = (
    st.columns(
        4,
        gap="medium",
    )
)


with feature_one:

    st.html(
        """
<div class="bp-feature-card">

    <div class="bp-feature-icon feature-green">
        🧠
    </div>

    <div class="bp-feature-title">
        Predictive Intelligence
    </div>

    <p class="bp-feature-text">

        Your trained DistilBERT model
        classifies individual and batch
        Spotify reviews as positive or
        negative sentiment.

    </p>

</div>
"""
    )


with feature_two:

    st.html(
        """
<div class="bp-feature-card">

    <div class="bp-feature-icon feature-blue">
        📊
    </div>

    <div class="bp-feature-title">
        Reputation Analytics
    </div>

    <p class="bp-feature-text">

        Sentiment predictions become
        brand-level indicators, issue
        distributions and customer-voice
        intelligence.

    </p>

</div>
"""
    )


with feature_three:

    st.html(
        """
<div class="bp-feature-card">

    <div class="bp-feature-icon feature-purple">
        🤖
    </div>

    <div class="bp-feature-title">
        AI Management Council
    </div>

    <p class="bp-feature-text">

        Five department managers analyse
        the same evidence through different
        organisational responsibilities.

    </p>

</div>
"""
    )


with feature_four:

    st.html(
        """
<div class="bp-feature-card">

    <div class="bp-feature-icon feature-pink">
        👔
    </div>

    <div class="bp-feature-title">
        Executive Intelligence
    </div>

    <p class="bp-feature-text">

        Gemini consolidates departmental
        findings into prioritised
        organisation-wide actions and
        measurable KPIs.

    </p>

</div>
"""
    )


st.write("")


# ============================================================
# MAIN NAVIGATION
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
            "the prediction produced by your "
            "deployed DistilBERT model."
        ),
    )


    input_column, prediction_column = (
        st.columns(
            [1.55, 1],
            gap="large",
        )
    )


    with input_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### ✍️ Customer Review"
            )


            review_text = (
                st.text_area(
                    "Customer review",
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


    with prediction_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 AI Prediction"
            )


            if not analyse_single:

                st.info(
                    "The DistilBERT prediction "
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
                        str(
                            result[
                                "sentiment"
                            ]
                        )
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
                            "that may negatively "
                            "influence brand perception."
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
                        )
                    )


                    st.caption(
                        "Confidence is the model's "
                        "output probability and does "
                        "not guarantee correctness."
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
            "Upload CSV or Excel reviews, "
            "run DistilBERT in batches and "
            "generate brand-level evidence."
        ),
    )


    upload_column, format_column = (
        st.columns(
            [1.55, 1],
            gap="large",
        )
    )


    with upload_column:

        with st.container(
            border=True
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


    with format_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📌 Expected Format"
            )


            st.write(
                "Your dataset needs at least "
                "one text column containing "
                "customer reviews."
            )


            st.code(
                "review_text\n"
                "Spotify is easy to use...\n"
                "The app keeps crashing...",
                language=None,
            )


    if uploaded_file is not None:

        try:

            file_name = (
                uploaded_file.name
                .lower()
            )


            if file_name.endswith(
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


            preview_column, information_column = (
                st.columns(
                    [3, 1],
                    gap="medium",
                )
            )


            with preview_column:

                st.markdown(
                    "### Dataset Preview"
                )


                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True,
                )


            with information_column:

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


            run_analysis = (
                st.button(
                    "🚀 Run Brand Intelligence Analysis",
                    type="primary",
                    width="stretch",
                    key="run_batch_analysis",
                )
            )


            if run_analysis:

                if (
                    len(valid_reviews)
                    == 0
                ):

                    st.warning(
                        "No valid reviews found."
                    )


                else:

                    try:

                        with st.status(
                            (
                                "Launching BrandPulse "
                                "analysis..."
                            ),
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
                                "📊 Calculating brand "
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
                                "🔎 Identifying customer "
                                "issue categories..."
                            )


                            st.session_state[
                                "prediction_results"
                            ] = analysed_df


                            st.session_state[
                                "analysis_summary"
                            ] = summary


                            # A new dataset means all
                            # previous LLM reports become
                            # invalid.
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
                "The uploaded file "
                "could not be read."
            )

            st.exception(
                error
            )


    # --------------------------------------------------------
    # PREDICTION TABLE
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
                "predictions and customer "
                "issue classifications."
            ),
        )


        display_results = (
            st.session_state[
                "prediction_results"
            ]
            .copy()
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
        )


        csv_output = (
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
            data=csv_output,
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
            "customer issues and customer-language "
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
            border=True
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

        metric_one, metric_two, metric_three, metric_four = (
            st.columns(
                4,
                gap="medium",
            )
        )


        with metric_one:

            kpi_card(
                "REVIEWS ANALYSED",
                f"{summary['total_reviews']:,}",
                "Current uploaded dataset",
                "kpi-blue",
            )


        with metric_two:

            kpi_card(
                "POSITIVE REVIEWS",
                f"{summary['positive_reviews']:,}",
                (
                    f"{summary['positive_percentage']}"
                    "% of classified reviews"
                ),
                "kpi-green",
            )


        with metric_three:

            kpi_card(
                "NEGATIVE REVIEWS",
                f"{summary['negative_reviews']:,}",
                (
                    f"{summary['negative_percentage']}"
                    "% of classified reviews"
                ),
                "kpi-red",
            )


        with metric_four:

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
            reputation_label,
            reputation_icon,
            reputation_color,
        ) = get_reputation_status(
            score
        )


        st.html(
            f"""
<div class="bp-reputation-panel">

    <div class="bp-reputation-label">
        CURRENT BRAND REPUTATION
    </div>

    <div
        class="bp-reputation-title"
        style="
            color:{reputation_color};
        "
    >
        {reputation_icon}
        {reputation_label}
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
            )
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
                border=True
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


                sentiment_figure = (
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


                sentiment_figure.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                )


                sentiment_figure.update_layout(
                    margin=dict(
                        l=5,
                        r=5,
                        t=10,
                        b=5,
                    ),

                    legend_title_text="",

                    paper_bgcolor=(
                        "rgba(0,0,0,0)"
                    ),

                    plot_bgcolor=(
                        "rgba(0,0,0,0)"
                    ),
                )


                st.plotly_chart(
                    sentiment_figure,
                    width="stretch",
                )


        with issue_column:

            with st.container(
                border=True
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
                        issue_df.sort_values(
                            "Mentions",
                            ascending=True,
                        )
                    )


                    issue_figure = (
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


                    issue_figure.update_layout(
                        coloraxis_showscale=False,

                        margin=dict(
                            l=5,
                            r=5,
                            t=10,
                            b=5,
                        ),

                        paper_bgcolor=(
                            "rgba(0,0,0,0)"
                        ),

                        plot_bgcolor=(
                            "rgba(0,0,0,0)"
                        ),
                    )


                    st.plotly_chart(
                        issue_figure,
                        width="stretch",
                    )


                else:

                    st.success(
                        "No issue categories detected."
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
                border=True
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


                if not positive_words.empty:

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
                border=True
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


                if not negative_words.empty:

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
        # NEGATIVE REVIEW EXAMPLES
        # ----------------------------------------------------

        st.write("")


        section_header(
            "CUSTOMER ATTENTION",
            "Reviews Requiring Attention",
            (
                "Representative negative reviews "
                "help management understand the "
                "customer concerns behind the metrics."
            ),
        )


        negative_reviews = (
            summary[
                "sample_negative_reviews"
            ]
        )


        if negative_reviews:

            for (
                review_number,
                review,
            ) in enumerate(
                negative_reviews,
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
                "No negative reviews detected."
            )


        st.info(
            "The Brand Reputation Score is a "
            "project-defined indicator calculated "
            "from the proportion of positive "
            "DistilBERT predictions. It is not "
            "a universal industry brand-reputation "
            "metric."
        )


# ============================================================
# TAB 4 — AI MANAGEMENT COUNCIL
# ============================================================

with management_tab:

    section_header(
        "GENERATIVE AI",
        "AI Management Council",
        (
            "Five role-based AI managers analyse "
            "the structured reputation evidence "
            "from different organisational perspectives."
        ),
    )


    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )


    if summary is None:

        with st.container(
            border=True
        ):

            st.warning(
                "Run **Batch Intelligence** first. "
                "The AI managers require structured "
                "brand-reputation evidence."
            )


    else:

        # ----------------------------------------------------
        # ARCHITECTURE
        # ----------------------------------------------------

        architecture_text, architecture_table = (
            st.columns(
                [1.45, 1],
                gap="large",
            )
        )


        with architecture_text:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🏢 Council Architecture"
                )


                st.write(
                    "All managers receive the same "
                    "brand-reputation summary. "
                    "Different role instructions "
                    "make each manager analyse the "
                    "evidence from its own "
                    "departmental responsibility."
                )


        with architecture_table:

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
        # PROGRESS
        # ----------------------------------------------------

        completed_reports = len(
            st.session_state[
                "manager_reports"
            ]
        )


        total_managers = len(
            MANAGER_ROLES
        )


        completion_ratio = (
            completed_reports
            / total_managers
        )


        st.write("")


        progress_column, progress_metric = (
            st.columns(
                [3, 1],
                gap="medium",
            )
        )


        with progress_column:

            st.markdown(
                "### 📋 Management Council Progress"
            )


            st.progress(
                completion_ratio
            )


            st.caption(
                (
                    f"{completed_reports} of "
                    f"{total_managers} department "
                    "reports completed."
                )
            )


        with progress_metric:

            kpi_card(
                "REPORTS READY",
                (
                    f"{completed_reports}"
                    f"/{total_managers}"
                ),
                "Council completion",
                "kpi-purple",
            )


        st.write("")


        # ----------------------------------------------------
        # DEPARTMENT TABS
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


        manager_tabs = {
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


        for (
            manager_name,
            manager_tab,
        ) in manager_tabs.items():

            with manager_tab:

                visual = (
                    get_manager_visual(
                        manager_name
                    )
                )


                provider = (
                    MANAGER_PROVIDERS[
                        manager_name
                    ]
                )


                if provider == "gemini":

                    provider_label = (
                        "✨ Gemini"
                    )

                    provider_css = (
                        "provider-gemini"
                    )


                else:

                    provider_label = (
                        "🌐 OpenRouter Free"
                    )

                    provider_css = (
                        "provider-openrouter"
                    )


                st.html(
                    f"""
<div class="bp-manager-profile">

    <div class="bp-manager-top">

        <div
            class="
                bp-avatar
                {visual['avatar']}
            "
        >
            {visual['emoji']}
        </div>

        <div>

            <div class="bp-manager-name">
                {manager_name}
            </div>

            <div class="bp-manager-short">
                {visual['short']}
            </div>

        </div>

    </div>

    <span
        class="
            bp-provider
            {provider_css}
        "
    >
        {provider_label}
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


                manager_button_key = (
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
                    key=manager_button_key,
                ):

                    try:

                        with st.status(
                            (
                                f"{manager_name} "
                                "is analysing "
                                "the evidence..."
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
                                "from the departmental "
                                "perspective..."
                            )


                            st.write(
                                "💡 Developing actionable "
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


                            # Any change to a department
                            # report invalidates an older
                            # executive report.
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
                # EXISTING MANAGER REPORT
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
                        border=True
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

    🤖 Provider:
    {report_provider}

    &nbsp;•&nbsp;

    Model:
    {report_model}

</div>
"""
                        )


                        st.write("")


                        st.markdown(
                            manager_report[
                                "content"
                            ]
                        )


                    st.download_button(
                        (
                            "⬇️ Download "
                            f"{manager_name} Report"
                        ),
                        data=(
                            manager_report[
                                "content"
                            ]
                        ),
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
                            "for this report is shown above."
                        )


        # ====================================================
        # EXECUTIVE MANAGER
        # ====================================================

        st.divider()


        st.html(
            """
<div class="bp-executive">

    <div class="bp-badge">
        👔 EXECUTIVE INTELLIGENCE
    </div>

    <div
        style="
            color:#F8FAFC;
            font-size:29px;
            font-weight:900;
        "
    >
        Executive Manager
    </div>

    <div
        style="
            max-width:850px;
            margin-top:9px;
            color:#97A5B7;
            font-size:13px;
            line-height:1.65;
            overflow-wrap:break-word;
        "
    >

        Gemini consolidates all five
        departmental analyses into one
        prioritised organisation-wide
        brand reputation strategy.

    </div>

</div>
"""
        )


        current_reports = (
            st.session_state[
                "manager_reports"
            ]
        )


        report_count = len(
            current_reports
        )


        st.write("")


        readiness_text, readiness_card = (
            st.columns(
                [2, 1],
                gap="medium",
            )
        )


        with readiness_text:

            if (
                report_count
                == total_managers
            ):

                st.success(
                    "✅ All five department reports "
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
                        not in current_reports
                    ]
                )


                st.info(
                    (
                        f"**{len(missing_managers)}** "
                        "department report(s) "
                        "still need to be generated."
                    )
                )


                with st.expander(
                    "View reports still required"
                ):

                    for manager in (
                        missing_managers
                    ):

                        st.write(
                            f"• {manager}"
                        )


        with readiness_card:

            kpi_card(
                "EXECUTIVE READY",
                (
                    "YES"
                    if report_count
                    == total_managers
                    else "NOT YET"
                ),
                (
                    f"{report_count}/"
                    f"{total_managers} reports"
                ),
                (
                    "kpi-green"
                    if report_count
                    == total_managers
                    else "kpi-purple"
                ),
            )


        # ----------------------------------------------------
        # GENERATE EXECUTIVE REPORT
        # ----------------------------------------------------

        if (
            report_count
            == total_managers
        ):

            generate_executive_button = (
                st.button(
                    (
                        "👔 Generate Executive "
                        "Brand Reputation Report"
                    ),
                    type="primary",
                    width="stretch",
                    key="generate_executive",
                )
            )


            if generate_executive_button:

                try:

                    with st.status(
                        (
                            "Executive Manager is "
                            "consolidating intelligence..."
                        ),
                        expanded=True,
                    ) as status:

                        st.write(
                            "📚 Reading all five "
                            "department reports..."
                        )


                        st.write(
                            "🔗 Identifying repeated "
                            "and cross-department "
                            "reputation issues..."
                        )


                        st.write(
                            "🎯 Ranking immediate "
                            "and long-term actions..."
                        )


                        st.write(
                            "📏 Consolidating "
                            "management KPIs..."
                        )


                        st.write(
                            "📝 Preparing final "
                            "executive strategy..."
                        )


                        executive_report = (
                            generate_executive_report(
                                summary,
                                current_reports,
                            )
                        )


                        st.session_state[
                            "executive_report"
                        ] = executive_report


                        status.update(
                            label=(
                                "Executive Brand Reputation "
                                "Report completed."
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
        # EXECUTIVE REPORT DISPLAY
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
                    "of predictive analytics and "
                    "department-level AI intelligence."
                ),
            )


            with st.container(
                border=True
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

    &nbsp;•&nbsp;

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


            download_report_column, download_data_column = (
                st.columns(
                    2,
                    gap="medium",
                )
            )


            with download_report_column:

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


            with download_data_column:

                complete_analysis = {
                    "analysis_summary":
                        summary,

                    "department_reports":
                        current_reports,

                    "executive_report":
                        executive_report,
                }


                complete_json = (
                    json.dumps(
                        complete_analysis,
                        indent=2,
                        ensure_ascii=False,
                    )
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
