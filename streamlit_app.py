# ============================================================
# BRANDPULSE AI
# Spotify Brand Reputation Intelligence System
# ============================================================

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import (
    analyse_predictions
)

from src.distilbert_predictor import (
    predict_sentiment,
    predict_batch,
)

from src.llm_service import (
    call_gemini,
    call_openrouter,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BrandPulse AI",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.html(
    """
<style>

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}


/* HERO */

.hero {

    padding: 36px 40px;

    border-radius: 26px;

    margin-bottom: 24px;

    background:
        radial-gradient(
            circle at top right,
            rgba(29,185,84,0.30),
            transparent 38%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(31,111,235,0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #181D25,
            #101319
        );

    border:
        1px solid
        rgba(255,255,255,0.08);

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.25);
}


.hero-badge {

    display: inline-block;

    padding: 7px 13px;

    border-radius: 999px;

    background:
        rgba(29,185,84,0.13);

    border:
        1px solid
        rgba(29,185,84,0.30);

    color: #55E487;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 16px;
}


.hero-title {

    font-size: 46px;

    font-weight: 800;

    margin: 0;

    color: #F7F9FC;
}


.hero-highlight {
    color: #55E487;
}


.hero-subtitle {

    color: #A9B1BC;

    font-size: 16px;

    line-height: 1.7;

    max-width: 850px;

    margin-top: 16px;
}


/* FEATURE CARDS */

.feature-card {

    padding: 21px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            #171B22,
            #14181E
        );

    border:
        1px solid
        rgba(255,255,255,0.07);

    min-height: 160px;
}


.feature-icon {

    width: 45px;

    height: 45px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 13px;

    background:
        rgba(29,185,84,0.10);

    font-size: 23px;

    margin-bottom: 13px;
}


.feature-title {

    font-size: 17px;

    font-weight: 700;

    margin-bottom: 7px;
}


.feature-text {

    color: #9CA6B3;

    font-size: 13px;

    line-height: 1.6;
}


/* SIDEBAR */

.sidebar-brand {

    font-size: 23px;

    font-weight: 800;
}


.section-label {

    color: #7E8998;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.3px;

    text-transform: uppercase;
}


.status-online {

    display: inline-block;

    padding: 6px 11px;

    border-radius: 999px;

    color: #55E487;

    background:
        rgba(29,185,84,0.12);

    font-size: 12px;

    font-weight: 600;
}


/* REPUTATION */

.reputation-positive {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(29,185,84,0.10);

    color: #55E487;

    font-weight: 700;
}


.reputation-mixed {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(245,183,49,0.10);

    color: #F5B731;

    font-weight: 700;
}


.reputation-negative {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(255,76,76,0.10);

    color: #FF7070;

    font-weight: 700;
}


header[data-testid="stHeader"] {
    background: transparent;
}

</style>
"""
)


# ============================================================
# SECRET HELPER
# ============================================================

def read_secret(
    key,
    default="Not configured"
):

    try:
        return st.secrets[key]

    except Exception:
        return default


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_results" not in st.session_state:

    st.session_state[
        "prediction_results"
    ] = None


if "analysis_summary" not in st.session_state:

    st.session_state[
        "analysis_summary"
    ] = None


if "gemini_test_result" not in st.session_state:

    st.session_state[
        "gemini_test_result"
    ] = None


if "openrouter_test_result" not in st.session_state:

    st.session_state[
        "openrouter_test_result"
    ] = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
<div class="sidebar-brand">
    🎧 BrandPulse AI
</div>
"""
    )

    st.caption(
        "Brand Reputation "
        "Intelligence Platform"
    )

    st.divider()


    st.html(
        """
<div class="section-label">
    DEPLOYMENT MODEL
</div>
"""
    )


    st.markdown(
        "### DistilBERT"
    )


    st.html(
        """
<span class="status-online">
    ● Model Online
</span>
"""
    )


    st.divider()


    st.html(
        """
<div class="section-label">
    GENERATIVE AI
</div>
"""
    )


    st.write(
        "✨ Gemini 3.7 Flash"
    )

    st.write(
        "🌐 OpenRouter Free"
    )


    st.divider()


    st.html(
        """
<div class="section-label">
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
<div class="hero">

    <div class="hero-badge">
        AI BRAND INTELLIGENCE
    </div>

    <div class="hero-title">
        Brand<span class="hero-highlight">Pulse</span> AI
    </div>

    <p class="hero-subtitle">

        Transform Spotify customer reviews into
        actionable brand reputation intelligence
        using DistilBERT sentiment classification,
        customer issue analysis and AI-assisted
        management intelligence.

    </p>

</div>
"""
)


# ============================================================
# FEATURE CARDS
# ============================================================

feature1, feature2, feature3, feature4 = (
    st.columns(4)
)


with feature1:

    st.html(
        """
<div class="feature-card">

    <div class="feature-icon">
        🧠
    </div>

    <div class="feature-title">
        DistilBERT AI
    </div>

    <div class="feature-text">
        Transformer-based sentiment
        classification.
    </div>

</div>
"""
    )


with feature2:

    st.html(
        """
<div class="feature-card">

    <div class="feature-icon">
        📊
    </div>

    <div class="feature-title">
        Reputation Analytics
    </div>

    <div class="feature-text">
        Convert predictions into
        measurable reputation indicators.
    </div>

</div>
"""
    )


with feature3:

    st.html(
        """
<div class="feature-card">

    <div class="feature-icon">
        🔎
    </div>

    <div class="feature-title">
        Issue Intelligence
    </div>

    <div class="feature-text">
        Identify recurring customer
        complaints and issues.
    </div>

</div>
"""
    )


with feature4:

    st.html(
        """
<div class="feature-card">

    <div class="feature-icon">
        🤖
    </div>

    <div class="feature-title">
        Multi-LLM Intelligence
    </div>

    <div class="feature-text">
        Gemini and OpenRouter support
        management-level analysis.
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
    llm_test_tab
) = st.tabs(
    [
        "🧪 Single Review",
        "📂 Batch Intelligence",
        "📈 Reputation Dashboard",
        "🔌 LLM Connection Test",
    ]
)


# ============================================================
# TAB 1 — SINGLE REVIEW
# ============================================================

with single_tab:

    st.markdown(
        "## Review Sentiment Laboratory"
    )


    review_left, review_right = (
        st.columns(
            [1.5, 1]
        )
    )


    with review_left:

        with st.container(
            border=True
        ):

            review_text = (
                st.text_area(
                    "Customer Review",
                    height=180,
                    placeholder=(
                        "Example: The application "
                        "keeps crashing after "
                        "the latest update."
                    )
                )
            )


            analyse_single = (
                st.button(
                    "✨ Analyse Sentiment",
                    type="primary",
                    width="stretch"
                )
            )


    with review_right:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 AI Prediction"
            )


            if analyse_single:

                if not review_text.strip():

                    st.warning(
                        "Enter a review first."
                    )


                else:

                    try:

                        with st.spinner(
                            "Analysing..."
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
                            .lower()
                        )


                        confidence = (
                            result[
                                "confidence"
                            ]
                            * 100
                        )


                        if (
                            sentiment
                            == "positive"
                        ):

                            st.success(
                                "🟢 Positive"
                            )


                        elif (
                            sentiment
                            == "negative"
                        ):

                            st.error(
                                "🔴 Negative"
                            )


                        else:

                            st.info(
                                sentiment.title()
                            )


                        st.metric(
                            "Model Confidence",
                            f"{confidence:.2f}%"
                        )


                    except Exception as error:

                        st.exception(
                            error
                        )


            else:

                st.info(
                    "Prediction will "
                    "appear here."
                )


# ============================================================
# TAB 2 — BATCH
# ============================================================

with batch_tab:

    st.markdown(
        "## Batch Brand Intelligence"
    )


    uploaded_file = (
        st.file_uploader(
            "Upload customer-review data",
            type=[
                "csv",
                "xlsx"
            ]
        )
    )


    if uploaded_file is not None:

        try:

            if (
                uploaded_file.name
                .lower()
                .endswith(
                    ".csv"
                )
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


            st.dataframe(
                uploaded_df.head(10),
                width="stretch"
            )


            review_column = (
                st.selectbox(
                    "Select review column",
                    options=(
                        uploaded_df
                        .columns
                        .tolist()
                    )
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
                    valid_reviews != ""
                ]
            )


            st.metric(
                "Valid Reviews",
                f"{len(valid_reviews):,}"
            )


            if st.button(
                "🚀 Run Brand Intelligence Analysis",
                type="primary",
                width="stretch"
            ):

                try:

                    with st.status(
                        "Running analysis...",
                        expanded=True
                    ) as status:

                        st.write(
                            "🧠 DistilBERT "
                            "classification..."
                        )


                        predictions = (
                            predict_batch(
                                valid_reviews.tolist(),
                                batch_size=16
                            )
                        )


                        prediction_df = (
                            pd.DataFrame(
                                predictions
                            )
                        )


                        st.write(
                            "📊 Reputation analysis..."
                        )


                        (
                            analysed_df,
                            summary
                        ) = (
                            analyse_predictions(
                                prediction_df
                            )
                        )


                        st.session_state[
                            "prediction_results"
                        ] = analysed_df


                        st.session_state[
                            "analysis_summary"
                        ] = summary


                        status.update(
                            label=(
                                "Analysis complete"
                            ),
                            state="complete",
                            expanded=False
                        )


                except Exception as error:

                    st.exception(
                        error
                    )


        except Exception as error:

            st.exception(
                error
            )


    # RESULTS

    if (
        st.session_state[
            "prediction_results"
        ]
        is not None
    ):

        results = (
            st.session_state[
                "prediction_results"
            ].copy()
        )


        results[
            "confidence"
        ] = (
            results[
                "confidence"
            ]
            * 100
        ).round(2)


        st.dataframe(
            results,
            width="stretch"
        )


        csv_data = (
            results
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            "⬇️ Download Results",
            data=csv_data,
            file_name=(
                "brandpulse_results.csv"
            ),
            mime="text/csv"
        )


# ============================================================
# TAB 3 — DASHBOARD
# ============================================================

with dashboard_tab:

    st.markdown(
        "## Brand Reputation Intelligence"
    )


    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )


    if summary is None:

        st.info(
            "Run Batch Intelligence first."
        )


    else:

        m1, m2, m3, m4 = (
            st.columns(4)
        )


        m1.metric(
            "Reviews",
            summary[
                "total_reviews"
            ]
        )


        m2.metric(
            "Positive",
            summary[
                "positive_reviews"
            ]
        )


        m3.metric(
            "Negative",
            summary[
                "negative_reviews"
            ]
        )


        m4.metric(
            "Reputation Score",
            (
                f"{summary['reputation_score']}"
                "%"
            )
        )


        sentiment_df = (
            pd.DataFrame(
                {
                    "Sentiment": [
                        "Positive",
                        "Negative"
                    ],

                    "Reviews": [
                        summary[
                            "positive_reviews"
                        ],

                        summary[
                            "negative_reviews"
                        ]
                    ]
                }
            )
        )


        chart_left, chart_right = (
            st.columns(2)
        )


        with chart_left:

            sentiment_chart = (
                px.pie(
                    sentiment_df,
                    names="Sentiment",
                    values="Reviews",
                    hole=0.6
                )
            )


            st.plotly_chart(
                sentiment_chart,
                width="stretch"
            )


        with chart_right:

            issues = (
                summary[
                    "issue_counts"
                ]
            )


            if issues:

                issue_df = (
                    pd.DataFrame(
                        [
                            {
                                "Issue":
                                    issue,

                                "Mentions":
                                    count
                            }

                            for (
                                issue,
                                count
                            )
                            in issues.items()
                        ]
                    )
                )


                issue_chart = (
                    px.bar(
                        issue_df,
                        x="Mentions",
                        y="Issue",
                        orientation="h"
                    )
                )


                st.plotly_chart(
                    issue_chart,
                    width="stretch"
                )


        st.markdown(
            "### 💚 Positive Customer Voice"
        )


        st.dataframe(
            pd.DataFrame(
                summary[
                    "top_positive_words"
                ]
            ),
            width="stretch"
        )


        st.markdown(
            "### 🚨 Negative Customer Voice"
        )


        st.dataframe(
            pd.DataFrame(
                summary[
                    "top_negative_words"
                ]
            ),
            width="stretch"
        )


        st.info(
            "The Brand Reputation Score "
            "is a project-defined indicator "
            "rather than a universal "
            "industry standard."
        )


# ============================================================
# TAB 4 — LLM CONNECTION TEST
# ============================================================

with llm_test_tab:

    st.markdown(
        "## 🔌 LLM Connection Test"
    )


    st.caption(
        "Test the Gemini Interactions API "
        "and OpenRouter Free Router."
    )


    # --------------------------------------------------------
    # CURRENT CONFIG
    # --------------------------------------------------------

    provider1, provider2 = (
        st.columns(2)
    )


    with provider1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### ✨ Gemini"
            )


            st.write(
                "Configured Model"
            )


            st.code(
                read_secret(
                    "GEMINI_MODEL",
                    "Not configured"
                ),
                language=None
            )


            st.caption(
                "Uses Google's "
                "Interactions API."
            )


    with provider2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🌐 OpenRouter Free"
            )


            st.write(
                "Requested Router"
            )


            st.code(
                read_secret(
                    "OPENROUTER_MODEL",
                    "Not configured"
                ),
                language=None
            )


            st.caption(
                "The actual free model "
                "may change per request."
            )


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    test_prompt = (
        st.text_area(
            "Test Prompt",
            value=(
                "Reply with one short "
                "sentence confirming that "
                "the API connection works."
            ),
            height=100
        )
    )


    test_button = (
        st.button(
            "🚀 Test Gemini + OpenRouter",
            type="primary",
            width="stretch"
        )
    )


    # --------------------------------------------------------
    # RUN TESTS
    # --------------------------------------------------------

    if test_button:

        st.markdown(
            "## Test Results"
        )


        gemini_column, router_column = (
            st.columns(
                2,
                gap="large"
            )
        )


        # GEMINI

        with gemini_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### ✨ Gemini"
                )


                try:

                    with st.spinner(
                        "Testing Gemini..."
                    ):

                        result = (
                            call_gemini(

                                system_prompt=(
                                    "You are a "
                                    "connection-test "
                                    "assistant. "
                                    "Respond briefly."
                                ),

                                user_prompt=(
                                    test_prompt
                                )
                            )
                        )


                    st.success(
                        "Gemini connection "
                        "successful."
                    )


                    st.write(
                        result[
                            "content"
                        ]
                    )


                    st.metric(
                        "Model",
                        result[
                            "model"
                        ]
                    )


                    st.session_state[
                        "gemini_test_result"
                    ] = result


                except Exception as error:

                    st.session_state[
                        "gemini_test_result"
                    ] = None


                    st.error(
                        "Gemini connection failed."
                    )


                    st.exception(
                        error
                    )


        # OPENROUTER

        with router_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🌐 OpenRouter Free"
                )


                try:

                    with st.spinner(
                        "Testing OpenRouter..."
                    ):

                        result = (
                            call_openrouter(

                                system_prompt=(
                                    "You are a "
                                    "connection-test "
                                    "assistant. "
                                    "Respond briefly."
                                ),

                                user_prompt=(
                                    test_prompt
                                )
                            )
                        )


                    st.success(
                        "OpenRouter connection "
                        "successful."
                    )


                    st.write(
                        result[
                            "content"
                        ]
                    )


                    st.metric(
                        "Actual Model",
                        result[
                            "model"
                        ]
                    )


                    st.caption(
                        "Requested route: "
                        "openrouter/free"
                    )


                    st.session_state[
                        "openrouter_test_result"
                    ] = result


                except Exception as error:

                    st.session_state[
                        "openrouter_test_result"
                    ] = None


                    st.error(
                        "OpenRouter connection failed."
                    )


                    st.exception(
                        error
                    )


        # ----------------------------------------------------
        # OVERALL
        # ----------------------------------------------------

        if (
            st.session_state[
                "gemini_test_result"
            ]
            is not None

            and

            st.session_state[
                "openrouter_test_result"
            ]
            is not None
        ):

            st.success(
                "✅ Gemini and OpenRouter "
                "are both ready for the "
                "AI Management Council."
            )
