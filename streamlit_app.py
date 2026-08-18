# ============================================================
# BRANDPULSE AI
# Online Review-Based Brand Reputation Prediction
# Using NLP Techniques
#
# FINAL STREAMLIT APPLICATION
#
# Predictive AI:
#   DistilBERT
#
# Department LLMs:
#   Technical Manager        -> OpenRouter Free
#   Product Manager          -> Ollama Cloud
#   Customer Service Manager -> OpenRouter Free
#   Marketing Manager        -> Ollama Cloud
#   Subscription Manager     -> OpenRouter Free
#
# Executive:
#   Gemini
# ============================================================

from io import BytesIO
import json
import re

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

from src.report_export import (
    create_brandpulse_docx,
    create_brandpulse_pdf,
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
    --green-soft: #5EEA91;

    --blue: #38BDF8;

    --purple: #A855F7;

    --pink: #F472B6;

    --orange: #FB923C;

    --yellow: #FACC15;

    --red: #FB7185;

    --background: #090D14;

    --panel: #121923;

    --panel-light: #182231;

    --text-main: #F8FAFC;

    --text-soft: #AAB6C5;

    --text-muted: #748196;
}


/* ==========================================================
   APPLICATION
   ========================================================== */

.stApp {

    background:

        radial-gradient(
            circle at 4% 5%,
            rgba(168, 85, 247, 0.10),
            transparent 23%
        ),

        radial-gradient(
            circle at 96% 5%,
            rgba(30, 215, 96, 0.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 72% 88%,
            rgba(56, 189, 248, 0.07),
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

    margin-bottom: 24px;

    border-radius: 30px;

    background:

        radial-gradient(
            circle at 88% 15%,
            rgba(30, 215, 96, 0.31),
            transparent 28%
        ),

        radial-gradient(
            circle at 11% 100%,
            rgba(168, 85, 247, 0.23),
            transparent 38%
        ),

        linear-gradient(
            130deg,
            #111827 0%,
            #151A24 45%,
            #0E1821 100%
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


.bp-badge {

    display: inline-flex;

    align-items: center;

    gap: 7px;

    padding: 7px 13px;

    margin-bottom: 16px;

    border-radius: 999px;

    background:
        rgba(
            30,
            215,
            96,
            0.10
        );

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

    margin: 0;

    color: #F8FAFC;

    font-size:
        clamp(
            38px,
            4vw,
            55px
        );

    font-weight: 900;

    line-height: 1.05;
}


.bp-gradient {

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

    max-width: 930px;

    margin-top: 17px;

    margin-bottom: 0;

    color: #B5C0CE;

    font-size: 16px;

    line-height: 1.75;
}


.bp-chip-area {

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

    color: #DCE5EF;

    font-size: 12px;

    white-space: nowrap;
}


/* ==========================================================
   FEATURE CARDS
   ========================================================== */

.bp-feature {

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
        0.20s ease;
}


.bp-feature:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(
            30,
            215,
            96,
            0.34
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

    width: 47px;

    height: 47px;

    margin-bottom: 15px;

    border-radius: 15px;

    font-size: 23px;
}


.icon-green {

    background:
        rgba(
            30,
            215,
            96,
            0.14
        );
}


.icon-blue {

    background:
        rgba(
            56,
            189,
            248,
            0.15
        );
}


.icon-purple {

    background:
        rgba(
            168,
            85,
            247,
            0.17
        );
}


.icon-orange {

    background:
        rgba(
            251,
            146,
            60,
            0.16
        );
}


.bp-feature-title {

    margin-bottom: 9px;

    color: #F8FAFC;

    font-size: 16px;

    font-weight: 850;

    line-height: 1.3;

    overflow-wrap: break-word;
}


.bp-feature-text {

    margin: 0;

    color: #9DAABB;

    font-size: 13px;

    line-height: 1.62;

    white-space: normal;

    overflow-wrap: break-word;
}


/* ==========================================================
   SECTION
   ========================================================== */

.bp-section {

    margin:
        8px 0 19px 0;
}


.bp-kicker {

    color: #5EEA91;

    font-size: 11px;

    font-weight: 850;

    letter-spacing: 1.35px;
}


.bp-section-title {

    margin:
        4px 0 4px 0;

    color: #F8FAFC;

    font-size: 28px;

    font-weight: 900;
}


.bp-section-text {

    color: #8F9DAF;

    font-size: 13px;

    line-height: 1.55;
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

    margin-top: 3px;

    color: #8391A4;

    font-size: 12px;
}


.bp-label {

    margin-bottom: 6px;

    color: #6F7D90;

    font-size: 10px;

    font-weight: 850;

    letter-spacing: 1.35px;

    text-transform: uppercase;
}


.bp-online {

    display: inline-flex;

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

    font-weight: 750;
}


/* ==========================================================
   KPI
   ========================================================== */

.bp-kpi {

    position: relative;

    overflow: hidden;

    min-height: 126px;

    padding:
        20px
        20px
        20px
        24px;

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


.kpi-orange::before {
    background: #FB923C;
}


.bp-kpi-label {

    color: #8795A8;

    font-size: 11px;

    font-weight: 800;
}


.bp-kpi-value {

    margin-top: 9px;

    color: #F8FAFC;

    font-size: 30px;

    font-weight: 900;
}


.bp-kpi-note {

    margin-top: 4px;

    color: #69788A;

    font-size: 11px;
}


/* ==========================================================
   REPUTATION PANEL
   ========================================================== */

.bp-reputation {

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


.bp-rep-label {

    color: #8796A9;

    font-size: 11px;

    font-weight: 800;
}


.bp-rep-title {

    margin-top: 6px;

    font-size: 24px;

    font-weight: 900;
}


/* ==========================================================
   MANAGER CARDS
   ========================================================== */

.bp-manager {

    box-sizing: border-box;

    width: 100%;

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

    font-weight: 900;
}


.bp-manager-short {

    margin-top: 2px;

    color: #8492A5;

    font-size: 12px;

    overflow-wrap: break-word;
}


/* ==========================================================
   PROVIDER BADGES
   ========================================================== */

.bp-provider {

    display: inline-block;

    margin-top: 12px;

    padding: 5px 9px;

    border-radius: 9px;

    font-size: 11px;

    font-weight: 800;
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


.provider-ollama {

    color: #FDBA74;

    background:
        rgba(
            249,
            115,
            22,
            0.12
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


/* ==========================================================
   REPORT
   ========================================================== */

.bp-report-source {

    display: inline-flex;

    flex-wrap: wrap;

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
   REPORT EXPORT
   ========================================================== */

.bp-export {

    padding: 25px;

    margin-top: 18px;

    border-radius: 24px;

    background:

        radial-gradient(
            circle at top right,
            rgba(56, 189, 248, 0.14),
            transparent 35%
        ),

        radial-gradient(
            circle at bottom left,
            rgba(30, 215, 96, 0.12),
            transparent 35%
        ),

        rgba(
            18,
            26,
            38,
            0.97
        );

    border:
        1px solid rgba(
            56,
            189,
            248,
            0.15
        );
}


.bp-export-title {

    color: #F8FAFC;

    font-size: 23px;

    font-weight: 900;
}


.bp-export-text {

    max-width: 850px;

    margin-top: 7px;

    color: #8D9CAF;

    font-size: 13px;

    line-height: 1.6;
}


/* ==========================================================
   ERROR PANEL
   ========================================================== */

.bp-error {

    padding: 18px;

    border-radius: 16px;

    background:
        rgba(
            251,
            113,
            133,
            0.08
        );

    border:
        1px solid rgba(
            251,
            113,
            133,
            0.20
        );
}


/* ==========================================================
   STREAMLIT
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

    font-weight: 800;
}


div[data-testid="stDownloadButton"]
> button {

    border-radius: 12px;

    font-weight: 750;
}


/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (
    max-width: 1200px
) {

    .bp-feature {

        min-height: 240px;
    }
}


@media (
    max-width: 800px
) {

    .bp-hero {

        padding: 30px 24px;
    }


    .bp-feature {

        min-height: 185px;
    }


    .bp-title {

        font-size: 38px;
    }
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
    description,
):

    st.html(
        f"""
<div class="bp-section">

    <div class="bp-kicker">
        {kicker}
    </div>

    <div class="bp-section-title">
        {title}
    </div>

    <div class="bp-section-text">
        {description}
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


def provider_display_name(
    provider,
):

    provider_names = {

        "gemini":
            "Gemini",

        "openrouter":
            "OpenRouter Free",

        "ollama":
            "Ollama Cloud",
    }


    return provider_names.get(
        str(provider).lower(),
        str(provider).title(),
    )


def provider_badge(
    provider,
):

    provider = (
        str(provider)
        .strip()
        .lower()
    )


    if provider == "gemini":

        return (
            "✨ Gemini",
            "provider-gemini",
        )


    if provider == "openrouter":

        return (
            "🌐 OpenRouter Free",
            "provider-openrouter",
        )


    if provider == "ollama":

        return (
            "🦙 Ollama Cloud",
            "provider-ollama",
        )


    return (
        provider.title(),
        "",
    )


def manager_visual(
    manager_name,
):

    styles = {

        "Technical Manager": {

            "emoji":
                "🛠️",

            "avatar":
                "avatar-tech",

            "short":
                (
                    "Reliability, software quality, "
                    "performance and technical issues"
                ),
        },


        "Product Manager": {

            "emoji":
                "🧩",

            "avatar":
                "avatar-product",

            "short":
                (
                    "Product experience, features, "
                    "usability and improvement priorities"
                ),
        },


        "Customer Service Manager": {

            "emoji":
                "🎧",

            "avatar":
                "avatar-service",

            "short":
                (
                    "Complaints, satisfaction, support "
                    "and customer service recovery"
                ),
        },


        "Marketing Manager": {

            "emoji":
                "📣",

            "avatar":
                "avatar-marketing",

            "short":
                (
                    "Brand perception, messaging, "
                    "reputation strengths and risks"
                ),
        },


        "Subscription Manager": {

            "emoji":
                "💳",

            "avatar":
                "avatar-subscription",

            "short":
                (
                    "Premium, pricing, advertisements, "
                    "billing and customer value"
                ),
        },
    }


    return styles[
        manager_name
    ]


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


def reset_management_outputs():
    """
    Clear manager/executive/export outputs
    when a new review dataset is analysed.
    """

    st.session_state[
        "manager_reports"
    ] = {}


    st.session_state[
        "executive_report"
    ] = None


    st.session_state[
        "docx_export"
    ] = None


    st.session_state[
        "pdf_export"
    ] = None


def reset_report_exports():
    """
    Existing DOCX/PDF becomes outdated if
    manager/executive report changes.
    """

    st.session_state[
        "docx_export"
    ] = None


    st.session_state[
        "pdf_export"
    ] = None


def normalise_export_data(
    data,
):

    if data is None:

        return None


    if isinstance(
        data,
        bytes,
    ):

        return data


    if isinstance(
        data,
        bytearray,
    ):

        return bytes(
            data
        )


    if isinstance(
        data,
        BytesIO,
    ):

        data.seek(0)

        return data.getvalue()


    if hasattr(
        data,
        "getvalue",
    ):

        value = data.getvalue()


        if isinstance(
            value,
            bytearray,
        ):

            return bytes(
                value
            )


        return value


    return data


def format_percentage(
    value,
):

    try:

        return (
            f"{float(value):.2f}%"
        )

    except Exception:

        return (
            f"{value}%"
        )


def prepare_word_dataframe(
    word_data,
):
    """
    Handle either:
    [
        {"word": "...", "count": 2}
    ]

    or:
    [
        ("word", 2)
    ]
    """

    if not word_data:

        return pd.DataFrame(
            columns=[
                "Word",
                "Frequency",
            ]
        )


    if isinstance(
        word_data[0],
        dict,
    ):

        df = pd.DataFrame(
            word_data
        )


        rename_map = {

            "word":
                "Word",

            "count":
                "Frequency",
        }


        return df.rename(
            columns=rename_map
        )


    df = pd.DataFrame(
        word_data,
        columns=[
            "Word",
            "Frequency",
        ],
    )


    return df


def clean_error_message(
    error,
):

    message = str(
        error
    )


    lower = (
        message.lower()
    )


    # --------------------------------------------------------
    # GEMINI
    # --------------------------------------------------------

    if (
        "429"
        in message
        and
        (
            "gemini"
            in lower
            or
            "quota"
            in lower
        )
    ):

        retry_match = re.search(
            r"retry in ([0-9.]+)",
            lower,
        )


        retry_text = ""


        if retry_match:

            retry_text = (
                " Please wait approximately "
                f"{retry_match.group(1)} seconds "
                "before trying again."
            )


        return (
            "Gemini is temporarily unavailable because "
            "the current API quota or rate limit has "
            "been reached."
            + retry_text
        )


    # --------------------------------------------------------
    # OPENROUTER
    # --------------------------------------------------------

    if (
        "openrouter"
        in lower
        and
        "429"
        in message
    ):

        return (
            "OpenRouter Free has temporarily reached "
            "its request limit. Please wait and "
            "try this manager again later."
        )


    # --------------------------------------------------------
    # OLLAMA
    # --------------------------------------------------------

    if (
        "ollama"
        in lower
        and
        "429"
        in message
    ):

        return (
            "Ollama Cloud has temporarily reached "
            "its request limit. Please wait and "
            "try this manager again later."
        )


    if (
        "ollama"
        in lower
        and
        "404"
        in message
    ):

        return (
            "The configured Ollama model was not found. "
            "Check OLLAMA_MODEL in Streamlit Secrets."
        )


    if (
        "ollama"
        in lower
        and
        "502"
        in message
    ):

        return (
            "The selected Ollama Cloud model is "
            "temporarily unavailable. Please retry later."
        )


    # --------------------------------------------------------
    # GENERIC
    # --------------------------------------------------------

    return message[
        :700
    ]


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION_VALUES = {

    "prediction_results":
        None,

    "analysis_summary":
        None,

    "manager_reports":
        {},

    "executive_report":
        None,

    "docx_export":
        None,

    "pdf_export":
        None,
}


for (
    state_key,
    default_value,
) in DEFAULT_SESSION_VALUES.items():

    if (
        state_key
        not in st.session_state
    ):

        st.session_state[
            state_key
        ] = default_value


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
    Brand Reputation Intelligence Platform
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
        (
            "Fine-tuned binary sentiment "
            "classification model."
        )
    )


    st.html(
        """
<span class="bp-online">
    ● Model Ready
</span>
"""
    )


    st.divider()


    st.html(
        """
<div class="bp-label">
    MULTI-LLM COUNCIL
</div>
"""
    )


    st.write(
        "🌐 OpenRouter Free"
    )


    st.caption(
        (
            "Technical, Customer Service "
            "and Subscription Managers"
        )
    )


    st.write(
        "🦙 Ollama Cloud"
    )


    st.caption(
        (
            "Product and Marketing Managers"
        )
    )


    st.write(
        "✨ Gemini"
    )


    st.caption(
        "Executive Manager only"
    )


    st.divider()


    st.html(
        """
<div class="bp-label">
    REPORT EXPORT
</div>
"""
    )


    st.write(
        "📘 Microsoft Word"
    )


    st.write(
        "📕 PDF"
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
**01** · Review Input

**02** · DistilBERT Prediction

**03** · Reputation Analytics

**04** · Issue Intelligence

**05** · Multi-LLM Council

**06** · Gemini Executive

**07** · DOCX / PDF Export
"""
    )


    st.divider()


    st.caption(
        "Final Year Project"
    )


    st.caption(
        (
            "Online Review-Based Brand "
            "Reputation Prediction Using "
            "NLP Techniques"
        )
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
<div class="bp-hero">

    <div class="bp-badge">
        ✦ AI-POWERED BRAND INTELLIGENCE
    </div>

    <div class="bp-title">

        Brand<span class="bp-gradient">
            Pulse AI
        </span>

    </div>

    <p class="bp-subtitle">

        Transform Spotify customer reviews into
        decision-ready brand intelligence.
        DistilBERT performs sentiment prediction,
        analytical modules identify reputation
        patterns, and a multi-provider management
        council using OpenRouter, Ollama and Gemini
        converts the evidence into departmental
        and executive-level recommendations.

    </p>

    <div class="bp-chip-area">

        <span class="bp-chip">
            🧠 DistilBERT
        </span>

        <span class="bp-chip">
            🌐 OpenRouter Free
        </span>

        <span class="bp-chip">
            🦙 Ollama Cloud
        </span>

        <span class="bp-chip">
            ✨ Gemini
        </span>

        <span class="bp-chip">
            📊 Reputation Analytics
        </span>

        <span class="bp-chip">
            📑 DOCX / PDF
        </span>

    </div>

</div>
"""
)


# ============================================================
# FEATURE CARDS
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
<div class="bp-feature">

    <div class="bp-feature-icon icon-green">
        🧠
    </div>

    <div class="bp-feature-title">
        Predictive Intelligence
    </div>

    <p class="bp-feature-text">

        The deployed DistilBERT model classifies
        individual and batch Spotify customer
        reviews into positive or negative sentiment.

    </p>

</div>
"""
    )


with feature_2:

    st.html(
        """
<div class="bp-feature">

    <div class="bp-feature-icon icon-blue">
        📊
    </div>

    <div class="bp-feature-title">
        Reputation Analytics
    </div>

    <p class="bp-feature-text">

        Predictions are transformed into sentiment
        distributions, a project-defined Brand
        Reputation Score, issue categories and
        customer voice intelligence.

    </p>

</div>
"""
    )


with feature_3:

    st.html(
        """
<div class="bp-feature">

    <div class="bp-feature-icon icon-purple">
        🤖
    </div>

    <div class="bp-feature-title">
        Multi-LLM Management Council
    </div>

    <p class="bp-feature-text">

        OpenRouter and Ollama generate five
        role-specific department reports while
        distributing the generative AI workload
        across multiple providers.

    </p>

</div>
"""
    )


with feature_4:

    st.html(
        """
<div class="bp-feature">

    <div class="bp-feature-icon icon-orange">
        👔
    </div>

    <div class="bp-feature-title">
        Executive Intelligence
    </div>

    <p class="bp-feature-text">

        Gemini is reserved for final executive
        consolidation after all five department
        reports have been completed.

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
# TAB 1
# SINGLE REVIEW
# ============================================================

with single_tab:

    section_header(
        "DISTILBERT LAB",
        "Single Review Intelligence",
        (
            "Enter one Spotify review and inspect "
            "the sentiment prediction generated by "
            "the deployed DistilBERT model."
        ),
    )


    input_column, result_column = (
        st.columns(
            [
                1.55,
                1,
            ],
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
                (
                    "Enter an English-language "
                    "Spotify customer review."
                )
            )


            analyse_single = (
                st.button(
                    "✨ Analyse Review",
                    type="primary",
                    width="stretch",
                    key="analyse_single",
                )
            )


    with result_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 DistilBERT Prediction"
            )


            if not analyse_single:

                st.info(
                    (
                        "The sentiment prediction "
                        "will appear here."
                    )
                )


            elif not review_text.strip():

                st.warning(
                    (
                        "Enter a review before "
                        "running the analysis."
                    )
                )


            else:

                try:

                    with st.spinner(
                        (
                            "DistilBERT is analysing "
                            "the review..."
                        )
                    ):

                        result = (
                            predict_sentiment(
                                review_text
                            )
                        )


                    # distilbert_predictor.py returns
                    # predicted_sentiment.
                    sentiment = (
                        str(
                            result.get(
                                "predicted_sentiment",
                                result.get(
                                    "sentiment",
                                    "unknown",
                                ),
                            )
                        )
                        .strip()
                        .lower()
                    )


                    confidence = (
                        float(
                            result.get(
                                "confidence",
                                0,
                            )
                        )
                        * 100
                    )


                    if sentiment == "positive":

                        st.success(
                            "🟢 Positive Sentiment"
                        )


                        st.write(
                            (
                                "The review reflects "
                                "a favourable customer "
                                "experience."
                            )
                        )


                    elif sentiment == "negative":

                        st.error(
                            "🔴 Negative Sentiment"
                        )


                        st.write(
                            (
                                "The review indicates "
                                "customer dissatisfaction "
                                "that may negatively "
                                "influence brand perception."
                            )
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
                        (
                            "Confidence represents the "
                            "model output probability "
                            "and does not guarantee "
                            "prediction correctness."
                        )
                    )


                except Exception as error:

                    st.error(
                        (
                            "The review could not "
                            "be analysed."
                        )
                    )


                    st.warning(
                        clean_error_message(
                            error
                        )
                    )


# ============================================================
# TAB 2
# BATCH INTELLIGENCE
# ============================================================

with batch_tab:

    section_header(
        "BATCH ANALYSIS",
        "Customer Review Intelligence",
        (
            "Upload a CSV or XLSX file, select the "
            "review-text column and classify multiple "
            "customer reviews using DistilBERT."
        ),
    )


    upload_column, guide_column = (
        st.columns(
            [
                1.55,
                1,
            ],
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
                (
                    "Supported formats: "
                    "CSV and XLSX."
                )
            )


    with guide_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📌 Expected Format"
            )


            st.write(
                (
                    "The dataset needs at least "
                    "one column containing "
                    "customer review text."
                )
            )


            st.code(
                (
                    "review_text\n"
                    "Spotify is easy to use...\n"
                    "The app keeps crashing..."
                ),
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


            preview_column, info_column = (
                st.columns(
                    [
                        3,
                        1,
                    ],
                    gap="medium",
                )
            )


            with preview_column:

                st.markdown(
                    "### Dataset Preview"
                )


                st.dataframe(
                    uploaded_df.head(
                        10
                    ),
                    width="stretch",
                    hide_index=True,
                )


            with info_column:

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
                    key="review_column_selector",
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


            if len(
                valid_reviews
            ) > 5000:

                st.warning(
                    (
                        "This dataset contains more "
                        "than 5,000 valid reviews. "
                        "Large-scale inference may "
                        "require significant processing "
                        "time and memory on Streamlit "
                        "Community Cloud. Consider using "
                        "a representative sample for "
                        "the live demonstration."
                    )
                )


            run_batch = (
                st.button(
                    (
                        "🚀 Run Brand Intelligence "
                        "Analysis"
                    ),
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
                        "No valid reviews were found."
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
                                (
                                    "🧠 Running DistilBERT "
                                    "sentiment classification..."
                                )
                            )


                            predictions = (
                                predict_batch(
                                    valid_reviews.tolist(),
                                    batch_size=16,
                                )
                            )


                            prediction_df = (
                                pd.DataFrame(
                                    predictions
                                )
                            )


                            st.write(
                                (
                                    "📊 Calculating brand "
                                    "reputation indicators..."
                                )
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
                                (
                                    "🔎 Detecting customer "
                                    "issue categories..."
                                )
                            )


                            st.write(
                                (
                                    "💬 Extracting customer "
                                    "voice information..."
                                )
                            )


                            st.session_state[
                                "prediction_results"
                            ] = analysed_df


                            st.session_state[
                                "analysis_summary"
                            ] = summary


                            # New evidence invalidates all
                            # previous management outputs.
                            reset_management_outputs()


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


                        st.warning(
                            clean_error_message(
                                error
                            )
                        )


        except Exception as error:

            st.error(
                (
                    "The uploaded file could "
                    "not be read."
                )
            )


            st.warning(
                clean_error_message(
                    error
                )
            )


    # ========================================================
    # PREDICTION TABLE
    # ========================================================

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
                "Review-level DistilBERT predictions "
                "and detected issue categories."
            ),
        )


        result_df = (
            st.session_state[
                "prediction_results"
            ].copy()
        )


        if (
            "confidence"
            in result_df.columns
        ):

            result_df[
                "confidence"
            ] = (
                result_df[
                    "confidence"
                ]
                .astype(float)
                .mul(100)
                .round(2)
            )


        result_df.rename(
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
            result_df,
            width="stretch",
            hide_index=True,
        )


        csv_data = (
            result_df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            "⬇️ Download Prediction Results",
            data=csv_data,
            file_name=(
                "brandpulse_prediction_results.csv"
            ),
            mime="text/csv",
            width="stretch",
        )


# ============================================================
# TAB 3
# REPUTATION DASHBOARD
# ============================================================

with dashboard_tab:

    section_header(
        "REPUTATION INTELLIGENCE",
        "Brand Reputation Dashboard",
        (
            "Explore aggregated sentiment, issue "
            "mentions, customer-language patterns "
            "and the project-defined reputation score."
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
                (
                    "Run **Batch Intelligence** "
                    "first to generate the "
                    "Reputation Dashboard."
                )
            )


    else:

        score = float(
            summary.get(
                "reputation_score",
                0,
            )
        )


        # ====================================================
        # KPIs
        # ====================================================

        metric_1, metric_2, metric_3, metric_4 = (
            st.columns(
                4,
                gap="medium",
            )
        )


        with metric_1:

            kpi_card(
                "REVIEWS ANALYSED",
                f"{summary.get('total_reviews', 0):,}",
                "Current analysis dataset",
                "kpi-blue",
            )


        with metric_2:

            kpi_card(
                "POSITIVE REVIEWS",
                f"{summary.get('positive_reviews', 0):,}",
                (
                    format_percentage(
                        summary.get(
                            "positive_percentage",
                            0,
                        )
                    )
                ),
                "kpi-green",
            )


        with metric_3:

            kpi_card(
                "NEGATIVE REVIEWS",
                f"{summary.get('negative_reviews', 0):,}",
                (
                    format_percentage(
                        summary.get(
                            "negative_percentage",
                            0,
                        )
                    )
                ),
                "kpi-red",
            )


        with metric_4:

            kpi_card(
                "REPUTATION SCORE",
                f"{score:.2f}%",
                "Project-defined indicator",
                "kpi-purple",
            )


        st.write("")


        # ====================================================
        # REPUTATION STATUS
        # ====================================================

        (
            status_label,
            status_icon,
            status_color,
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
        style="color:{status_color};"
    >
        {status_icon}
        {status_label}
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


        st.caption(
            (
                "The Brand Reputation Score is "
                "calculated from the proportion "
                "of positive DistilBERT predictions."
            )
        )


        st.write("")


        # ====================================================
        # CHARTS
        # ====================================================

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

                                summary.get(
                                    "positive_reviews",
                                    0,
                                ),

                                summary.get(
                                    "negative_reviews",
                                    0,
                                ),
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
                )


                sentiment_chart.update_layout(

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
                    sentiment_chart,
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
                    summary.get(
                        "issue_counts",
                        {},
                    )
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
                        issue_chart,
                        width="stretch",
                    )


                    st.caption(
                        (
                            "Issue values represent "
                            "detected issue mentions. "
                            "A review may contain more "
                            "than one issue."
                        )
                    )


                else:

                    st.success(
                        (
                            "No negative-review issue "
                            "categories were detected."
                        )
                    )


        # ====================================================
        # CUSTOMER VOICE
        # ====================================================

        st.write("")


        section_header(
            "VOICE OF CUSTOMER",
            "Customer Language Intelligence",
            (
                "Frequently occurring terms in "
                "positive and negative predicted reviews."
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
                    prepare_word_dataframe(
                        summary.get(
                            "top_positive_words",
                            [],
                        )
                    )
                )


                if not positive_words.empty:

                    st.dataframe(
                        positive_words,
                        width="stretch",
                        hide_index=True,
                    )


                else:

                    st.info(
                        (
                            "No positive-word "
                            "data are available."
                        )
                    )


        with negative_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 💗 Negative Customer Voice"
                )


                negative_words = (
                    prepare_word_dataframe(
                        summary.get(
                            "top_negative_words",
                            [],
                        )
                    )
                )


                if not negative_words.empty:

                    st.dataframe(
                        negative_words,
                        width="stretch",
                        hide_index=True,
                    )


                else:

                    st.info(
                        (
                            "No negative-word "
                            "data are available."
                        )
                    )


        # ====================================================
        # REPRESENTATIVE NEGATIVE REVIEWS
        # ====================================================

        st.write("")


        section_header(
            "CUSTOMER ATTENTION",
            "Reviews Requiring Attention",
            (
                "Representative negative reviews "
                "provide customer context behind "
                "the aggregate indicators."
            ),
        )


        negative_reviews = (
            summary.get(
                "sample_negative_reviews",
                [],
            )
        )


        if negative_reviews:

            for (
                index,
                review,
            ) in enumerate(
                negative_reviews,
                start=1,
            ):

                with st.expander(
                    (
                        "🚨 Negative Review "
                        f"{index}"
                    )
                ):

                    st.write(
                        review
                    )


        else:

            st.success(
                (
                    "No representative negative "
                    "reviews are available."
                )
            )


        st.info(
            (
                "The Brand Reputation Score is a "
                "project-defined decision-support "
                "indicator. It is not an official "
                "Spotify metric or a universal "
                "industry-standard reputation index."
            )
        )


# ============================================================
# TAB 4
# AI MANAGEMENT COUNCIL
# ============================================================

with management_tab:

    section_header(
        "MULTI-LLM DECISION SUPPORT",
        "AI Management Council",
        (
            "Five department managers interpret "
            "the same structured reputation evidence "
            "using OpenRouter and Ollama. Gemini is "
            "reserved for final executive consolidation."
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
                (
                    "Run **Batch Intelligence** first. "
                    "The AI Management Council requires "
                    "structured brand-reputation evidence."
                )
            )


    else:

        # ====================================================
        # PROVIDER ARCHITECTURE
        # ====================================================

        architecture_left, architecture_right = (
            st.columns(
                [
                    1.35,
                    1,
                ],
                gap="large",
            )
        )


        with architecture_left:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🏢 Multi-Provider Architecture"
                )


                st.write(
                    (
                        "The department-level workload is "
                        "distributed between OpenRouter "
                        "Free and Ollama Cloud. Gemini is "
                        "reserved for the final Executive "
                        "Manager to reduce dependency on "
                        "one provider and preserve Gemini "
                        "quota for consolidation."
                    )
                )


                st.markdown(
                    """
**Predictive AI**

🧠 DistilBERT

**Department AI**

🌐 OpenRouter Free  
🦙 Ollama Cloud

**Executive AI**

✨ Gemini
"""
                )


        with architecture_right:

            architecture_rows = []


            for (
                manager_name,
                provider,
            ) in MANAGER_PROVIDERS.items():

                architecture_rows.append(
                    {

                        "Manager":
                            manager_name,

                        "Provider":
                            provider_display_name(
                                provider
                            ),
                    }
                )


            architecture_rows.append(
                {

                    "Manager":
                        "Executive Manager",

                    "Provider":
                        "Gemini",
                }
            )


            architecture_df = (
                pd.DataFrame(
                    architecture_rows
                )
            )


            st.dataframe(
                architecture_df,
                width="stretch",
                hide_index=True,
            )


        # ====================================================
        # MANAGEMENT PROGRESS
        # ====================================================

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
            /
            total_managers
        )


        st.write("")


        progress_column, progress_card = (
            st.columns(
                [
                    3,
                    1,
                ],
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


        with progress_card:

            kpi_card(
                "REPORTS READY",
                (
                    f"{completed_reports}"
                    f"/{total_managers}"
                ),
                "Department reports",
                "kpi-purple",
            )


        # ====================================================
        # MANAGER TABS
        # ====================================================

        st.write("")


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


        # ====================================================
        # INDIVIDUAL MANAGERS
        # ====================================================

        for (
            manager_name,
            manager_tab,
        ) in manager_tabs.items():

            with manager_tab:

                visual = (
                    manager_visual(
                        manager_name
                    )
                )


                provider = (
                    MANAGER_PROVIDERS[
                        manager_name
                    ]
                )


                (
                    provider_label,
                    provider_class,
                ) = provider_badge(
                    provider
                )


                st.html(
                    f"""
<div class="bp-manager">

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
            {provider_class}
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


                existing_report = (
                    st.session_state[
                        "manager_reports"
                    ].get(
                        manager_name
                    )
                )


                # ------------------------------------------------
                # BUTTON TEXT
                # ------------------------------------------------

                if existing_report:

                    button_label = (
                        "🔄 Regenerate "
                        f"{manager_name} Report"
                    )


                else:

                    button_label = (
                        "✨ Generate "
                        f"{manager_name} Report"
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
                    button_label,
                    type="primary",
                    width="stretch",
                    key=button_key,
                ):

                    try:

                        with st.status(
                            (
                                f"{manager_name} is "
                                "analysing the evidence..."
                            ),
                            expanded=True,
                        ) as manager_status:

                            st.write(
                                (
                                    "📊 Reading brand "
                                    "reputation indicators..."
                                )
                            )


                            st.write(
                                (
                                    "🔎 Reviewing department-"
                                    "relevant customer issues..."
                                )
                            )


                            st.write(
                                (
                                    f"🤖 Connecting to "
                                    f"{provider_display_name(provider)}..."
                                )
                            )


                            st.write(
                                (
                                    "💡 Developing grounded "
                                    "management recommendations..."
                                )
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


                            # Manager changed -> old
                            # Executive Report is invalid.
                            st.session_state[
                                "executive_report"
                            ] = None


                            reset_report_exports()


                            manager_status.update(
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
                                f"{manager_name} report "
                                "generation failed."
                            )
                        )


                        st.warning(
                            clean_error_message(
                                error
                            )
                        )


                # ------------------------------------------------
                # DISPLAY EXISTING REPORT
                # ------------------------------------------------

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


                        requested_model = (
                            manager_report.get(
                                "requested_model"
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


                        if (
                            requested_model
                            and
                            requested_model
                            != report_model
                        ):

                            st.caption(
                                (
                                    "Requested route/model: "
                                    f"{requested_model}"
                                )
                            )


                        st.write("")


                        st.markdown(
                            manager_report.get(
                                "content",
                                "",
                            )
                        )


                    st.download_button(
                        (
                            "⬇️ Download "
                            f"{manager_name} Report"
                        ),
                        data=(
                            manager_report.get(
                                "content",
                                "",
                            )
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
                            (
                                "OpenRouter was requested "
                                "through `openrouter/free`. "
                                "The actual free model "
                                "returned by OpenRouter is "
                                "shown above."
                            )
                        )


                    if (
                        report_provider
                        == "Ollama"
                    ):

                        st.caption(
                            (
                                "This department report "
                                "was generated through "
                                "Ollama Cloud using the "
                                "configured Ollama model."
                            )
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
            max-width:880px;
            margin-top:9px;
            color:#97A5B7;
            font-size:13px;
            line-height:1.65;
        "
    >

        Gemini is reserved for the final
        consolidation stage. It receives the
        structured reputation evidence together
        with all five completed department reports
        and produces one organisation-wide
        executive strategy.

    </div>

    <span
        class="
            bp-provider
            provider-gemini
        "
    >
        ✨ Gemini — Executive Only
    </span>

</div>
"""
        )


        manager_reports = (
            st.session_state[
                "manager_reports"
            ]
        )


        report_count = len(
            manager_reports
        )


        st.write("")


        readiness_left, readiness_right = (
            st.columns(
                [
                    2,
                    1,
                ],
                gap="medium",
            )
        )


        with readiness_left:

            if (
                report_count
                == total_managers
            ):

                st.success(
                    (
                        "✅ All five department "
                        "reports are ready. Gemini "
                        "can now perform the final "
                        "Executive Manager call."
                    )
                )


            else:

                missing_managers = (
                    [
                        manager

                        for manager
                        in MANAGER_ROLES

                        if manager
                        not in manager_reports
                    ]
                )


                st.info(
                    (
                        f"**{len(missing_managers)}** "
                        "department report(s) are "
                        "still required before "
                        "Gemini is called."
                    )
                )


                with st.expander(
                    "View missing reports"
                ):

                    for manager in (
                        missing_managers
                    ):

                        provider = (
                            MANAGER_PROVIDERS[
                                manager
                            ]
                        )


                        st.write(
                            (
                                f"• {manager} — "
                                f"{provider_display_name(provider)}"
                            )
                        )


        with readiness_right:

            kpi_card(
                "GEMINI READY",
                (
                    "YES"
                    if report_count
                    == total_managers
                    else
                    "NOT YET"
                ),
                (
                    f"{report_count}/"
                    f"{total_managers} reports"
                ),
                (
                    "kpi-green"
                    if report_count
                    == total_managers
                    else
                    "kpi-purple"
                ),
            )


        # ====================================================
        # GENERATE EXECUTIVE REPORT
        # ====================================================

        if (
            report_count
            == total_managers
        ):

            existing_executive = (
                st.session_state[
                    "executive_report"
                ]
            )


            if existing_executive:

                executive_button_label = (
                    "🔄 Regenerate Executive "
                    "Brand Reputation Report"
                )


            else:

                executive_button_label = (
                    "👔 Generate Executive "
                    "Brand Reputation Report"
                )


            if st.button(
                executive_button_label,
                type="primary",
                width="stretch",
                key="generate_executive",
            ):

                try:

                    with st.status(
                        (
                            "Gemini Executive Manager "
                            "is consolidating intelligence..."
                        ),
                        expanded=True,
                    ) as executive_status:

                        st.write(
                            (
                                "📚 Reading all five "
                                "department reports..."
                            )
                        )


                        st.write(
                            (
                                "📊 Reviewing core brand "
                                "reputation evidence..."
                            )
                        )


                        st.write(
                            (
                                "🔗 Identifying cross-"
                                "department findings..."
                            )
                        )


                        st.write(
                            (
                                "🎯 Prioritising management "
                                "actions..."
                            )
                        )


                        st.write(
                            (
                                "📏 Consolidating executive "
                                "KPIs..."
                            )
                        )


                        st.write(
                            (
                                "✨ Calling Gemini for "
                                "final executive synthesis..."
                            )
                        )


                        executive_report = (
                            generate_executive_report(
                                summary,
                                manager_reports,
                            )
                        )


                        st.session_state[
                            "executive_report"
                        ] = executive_report


                        reset_report_exports()


                        executive_status.update(
                            label=(
                                "Executive Brand Reputation "
                                "Report completed."
                            ),
                            state="complete",
                            expanded=False,
                        )


                    st.toast(
                        (
                            "Executive report generated "
                            "successfully."
                        ),
                        icon="👔",
                    )


                except Exception as error:

                    st.error(
                        (
                            "Executive report generation "
                            "failed."
                        )
                    )


                    st.warning(
                        clean_error_message(
                            error
                        )
                    )


                    st.info(
                        (
                            "Your five department reports "
                            "remain stored. You do not need "
                            "to regenerate them before "
                            "retrying the Executive Manager."
                        )
                    )


        # ====================================================
        # EXECUTIVE REPORT DISPLAY
        # ====================================================

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
                    "Organisation-wide synthesis of "
                    "DistilBERT analytics and the five "
                    "department-level AI reports."
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
                    executive_report.get(
                        "content",
                        "",
                    )
                )


            # =================================================
            # RAW EXPORTS
            # =================================================

            raw_left, raw_right = (
                st.columns(
                    2,
                    gap="medium",
                )
            )


            with raw_left:

                st.download_button(
                    (
                        "⬇️ Download Executive "
                        "Markdown"
                    ),
                    data=(
                        executive_report.get(
                            "content",
                            "",
                        )
                    ),
                    file_name=(
                        "executive_brand_"
                        "reputation_report.md"
                    ),
                    mime="text/markdown",
                    width="stretch",
                )


            with raw_right:

                complete_package = {

                    "analysis_summary":
                        summary,

                    "department_reports":
                        manager_reports,

                    "executive_report":
                        executive_report,
                }


                complete_json = (
                    json.dumps(
                        complete_package,
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    )
                )


                st.download_button(
                    "📦 Download Complete JSON",
                    data=complete_json,
                    file_name=(
                        "brandpulse_complete_"
                        "analysis.json"
                    ),
                    mime="application/json",
                    width="stretch",
                )


            # =================================================
            # PROFESSIONAL REPORT CENTRE
            # =================================================

            st.write("")


            st.html(
                """
<div class="bp-export">

    <div class="bp-export-title">
        📑 Professional Report Centre
    </div>

    <div class="bp-export-text">

        Create both professional report formats
        from the same completed analysis. The
        Microsoft Word version supports editing,
        while the PDF provides a fixed-format
        report for presentation and sharing.

    </div>

</div>
"""
            )


            st.write("")


            prepare_reports = (
                st.button(
                    (
                        "⚡ Prepare DOCX + "
                        "PDF Reports"
                    ),
                    type="primary",
                    width="stretch",
                    key="prepare_both_reports",
                )
            )


            if prepare_reports:

                try:

                    with st.status(
                        (
                            "Preparing professional "
                            "reports..."
                        ),
                        expanded=True,
                    ) as export_status:

                        # -------------------------------------
                        # DOCX
                        # -------------------------------------

                        st.write(
                            (
                                "📘 Creating Microsoft "
                                "Word report..."
                            )
                        )


                        docx_result = (
                            create_brandpulse_docx(
                                analysis_summary=(
                                    summary
                                ),
                                manager_reports=(
                                    manager_reports
                                ),
                                executive_report=(
                                    executive_report
                                ),
                            )
                        )


                        st.session_state[
                            "docx_export"
                        ] = (
                            normalise_export_data(
                                docx_result
                            )
                        )


                        st.write(
                            "✅ Word report prepared."
                        )


                        # -------------------------------------
                        # PDF
                        # -------------------------------------

                        st.write(
                            (
                                "📕 Creating PDF "
                                "report..."
                            )
                        )


                        pdf_result = (
                            create_brandpulse_pdf(
                                analysis_summary=(
                                    summary
                                ),
                                manager_reports=(
                                    manager_reports
                                ),
                                executive_report=(
                                    executive_report
                                ),
                            )
                        )


                        st.session_state[
                            "pdf_export"
                        ] = (
                            normalise_export_data(
                                pdf_result
                            )
                        )


                        st.write(
                            "✅ PDF report prepared."
                        )


                        export_status.update(
                            label=(
                                "DOCX and PDF reports "
                                "are ready."
                            ),
                            state="complete",
                            expanded=False,
                        )


                    st.toast(
                        (
                            "Both professional reports "
                            "are ready."
                        ),
                        icon="📑",
                    )


                except Exception as error:

                    st.session_state[
                        "docx_export"
                    ] = None


                    st.session_state[
                        "pdf_export"
                    ] = None


                    st.error(
                        (
                            "Professional report "
                            "generation failed."
                        )
                    )


                    st.warning(
                        clean_error_message(
                            error
                        )
                    )


            # =================================================
            # PROFESSIONAL DOWNLOADS
            # =================================================

            docx_data = (
                st.session_state[
                    "docx_export"
                ]
            )


            pdf_data = (
                st.session_state[
                    "pdf_export"
                ]
            )


            if (
                docx_data is not None
                and
                pdf_data is not None
            ):

                st.success(
                    (
                        "✅ Both professional "
                        "report formats are ready."
                    )
                )


                docx_column, pdf_column = (
                    st.columns(
                        2,
                        gap="large",
                    )
                )


                with docx_column:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### 📘 Word Report"
                        )


                        st.write(
                            (
                                "Editable `.docx` report "
                                "containing the complete "
                                "BrandPulse analysis."
                            )
                        )


                        st.download_button(
                            (
                                "📘 Download Complete "
                                "Word Report"
                            ),
                            data=docx_data,
                            file_name=(
                                "BrandPulse_AI_"
                                "Brand_Reputation_"
                                "Report.docx"
                            ),
                            mime=(
                                "application/"
                                "vnd.openxmlformats-"
                                "officedocument."
                                "wordprocessingml.document"
                            ),
                            width="stretch",
                            key="download_docx",
                        )


                with pdf_column:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### 📕 PDF Report"
                        )


                        st.write(
                            (
                                "Fixed-format `.pdf` report "
                                "containing the complete "
                                "BrandPulse analysis."
                            )
                        )


                        st.download_button(
                            (
                                "📕 Download Complete "
                                "PDF Report"
                            ),
                            data=pdf_data,
                            file_name=(
                                "BrandPulse_AI_"
                                "Brand_Reputation_"
                                "Report.pdf"
                            ),
                            mime="application/pdf",
                            width="stretch",
                            key="download_pdf",
                        )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.divider()

st.caption(
    (
        "BrandPulse AI · Academic Final Year Project Prototype · "
        "DistilBERT sentiment prediction + Python reputation "
        "analytics + OpenRouter/Ollama department intelligence "
        "+ Gemini executive consolidation."
    )
)
