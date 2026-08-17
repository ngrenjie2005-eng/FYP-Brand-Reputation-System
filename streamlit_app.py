# ============================================================
# BRANDPULSE AI
# Spotify Brand Reputation Intelligence System
# ============================================================

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import analyse_predictions

from src.distilbert_predictor import (
    predict_sentiment,
    predict_batch
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BrandPulse AI",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
<style>

/* ==========================================================
   MAIN PAGE
   ========================================================== */

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    padding: 36px 40px;
    border-radius: 26px;
    margin-bottom: 24px;

    background:
        radial-gradient(
            circle at top right,
            rgba(29, 185, 84, 0.30),
            transparent 38%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(31, 111, 235, 0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #181D25,
            #101319
        );

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.08
        );

    box-shadow:
        0 15px 40px rgba(
            0,
            0,
            0,
            0.25
        );
}


.hero-badge {
    display: inline-block;

    padding: 7px 13px;

    border-radius: 999px;

    background:
        rgba(29, 185, 84, 0.13);

    border:
        1px solid rgba(
            29,
            185,
            84,
            0.30
        );

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

    line-height: 1.05;

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
    margin-bottom: 0;
}


/* ==========================================================
   FEATURE CARDS
   ========================================================== */

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
        1px solid rgba(
            255,
            255,
            255,
            0.07
        );

    min-height: 160px;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}


.feature-card:hover {

    transform: translateY(-3px);

    border-color:
        rgba(
            29,
            185,
            84,
            0.45
        );
}


.feature-icon {

    width: 45px;
    height: 45px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 13px;

    background:
        rgba(
            29,
            185,
            84,
            0.10
        );

    font-size: 23px;

    margin-bottom: 13px;
}


.feature-title {

    font-size: 17px;

    font-weight: 700;

    margin-bottom: 7px;

    color: #F3F5F7;
}


.feature-text {

    color: #9CA6B3;

    font-size: 13px;

    line-height: 1.6;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

.sidebar-brand {

    font-size: 23px;

    font-weight: 800;

    margin-bottom: 3px;
}


.sidebar-subtitle {

    color: #919BA8;

    font-size: 12px;

    margin-bottom: 15px;
}


.section-label {

    color: #7E8998;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.3px;

    text-transform: uppercase;

    margin-bottom: 4px;
}


.status-online {

    display: inline-block;

    padding: 6px 11px;

    border-radius: 999px;

    color: #55E487;

    background:
        rgba(
            29,
            185,
            84,
            0.12
        );

    border:
        1px solid rgba(
            29,
            185,
            84,
            0.20
        );

    font-size: 12px;

    font-weight: 600;
}


/* ==========================================================
   INFORMATION TEXT
   ========================================================== */

.hint-text {

    color: #8993A0;

    font-size: 13px;
}


/* ==========================================================
   REPUTATION LABEL
   ========================================================== */

.reputation-positive {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(
            29,
            185,
            84,
            0.10
        );

    border:
        1px solid rgba(
            29,
            185,
            84,
            0.20
        );

    color: #55E487;

    font-weight: 700;
}


.reputation-mixed {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(
            245,
            183,
            49,
            0.10
        );

    border:
        1px solid rgba(
            245,
            183,
            49,
            0.20
        );

    color: #F5B731;

    font-weight: 700;
}


.reputation-negative {

    padding: 13px 17px;

    border-radius: 12px;

    background:
        rgba(
            255,
            76,
            76,
            0.10
        );

    border:
        1px solid rgba(
            255,
            76,
            76,
            0.20
        );

    color: #FF7070;

    font-weight: 700;
}


/* ==========================================================
   STREAMLIT SMALL IMPROVEMENTS
   ========================================================== */

header[data-testid="stHeader"] {
    background: transparent;
}


/* Make tabs easier to read */

button[data-baseweb="tab"] {

    font-size: 14px;

    font-weight: 600;
}


/* Dataframe rounding */

[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;
}


/* File uploader */

[data-testid="stFileUploader"] {

    border-radius: 16px;
}

</style>
"""
)


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


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
<div class="sidebar-brand">
    🎧 BrandPulse AI
</div>

<div class="sidebar-subtitle">
    Brand Reputation Intelligence Platform
</div>
"""
    )

    st.divider()


    # --------------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------------

    st.html(
        """
<div class="section-label">
    DEPLOYMENT MODEL
</div>
"""
    )

    st.markdown("### DistilBERT")

    st.caption(
        "Transformer-based binary "
        "sentiment classification"
    )

    st.html(
        """
<span class="status-online">
    ● Model Online
</span>
"""
    )


    st.divider()


    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.html(
        """
<div class="section-label">
    SYSTEM PIPELINE
</div>
"""
    )

    st.markdown(
        """
**1.** Upload customer reviews

**2.** DistilBERT sentiment prediction

**3.** Brand reputation analysis

**4.** Customer issue detection

**5.** Management intelligence
"""
    )


    st.divider()


    # --------------------------------------------------------
    # PROJECT INFORMATION
    # --------------------------------------------------------

    st.caption(
        "Final Year Project"
    )

    st.caption(
        "Online Review-Based Brand "
        "Reputation Prediction Using "
        "NLP Techniques"
    )


# ============================================================
# HERO SECTION
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
        Transform Spotify customer reviews into actionable
        brand reputation intelligence using DistilBERT sentiment
        classification, customer issue analysis and AI-assisted
        management insights.
    </p>

</div>
"""
)


# ============================================================
# FEATURE CARDS
# ============================================================

feature1, feature2, feature3, feature4 = (
    st.columns(
        4,
        gap="medium"
    )
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
        Transformer-based sentiment classification
        identifies positive and negative customer
        opinions.
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
        Convert sentiment predictions into measurable
        brand reputation indicators and customer
        sentiment summaries.
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
        Identify common technical, subscription,
        playback and customer experience problems
        from negative reviews.
    </div>

</div>
"""
    )


with feature4:

    st.html(
        """
<div class="feature-card">

    <div class="feature-icon">
        💡
    </div>

    <div class="feature-title">
        AI Management
    </div>

    <div class="feature-text">
        Role-based LLM department managers will later
        transform findings into business recommendations.
    </div>

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
    dashboard_tab
) = st.tabs(
    [
        "🧪 Single Review",
        "📂 Batch Intelligence",
        "📈 Reputation Dashboard"
    ]
)


# ============================================================
# TAB 1
# SINGLE REVIEW
# ============================================================

with single_tab:

    st.markdown(
        "## Review Sentiment Laboratory"
    )

    st.caption(
        "Test the deployed DistilBERT model "
        "using an individual Spotify review."
    )


    left_column, right_column = (
        st.columns(
            [1.6, 1],
            gap="large"
        )
    )


    # --------------------------------------------------------
    # REVIEW INPUT
    # --------------------------------------------------------

    with left_column:

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
                        "Example: Spotify keeps "
                        "crashing after the latest "
                        "update and playback randomly "
                        "stops."
                    ),
                    height=190,
                    label_visibility="collapsed"
                )
            )

            st.html(
                """
<span class="hint-text">
    Enter an English-language Spotify review.
</span>
"""
            )

            st.write("")

            predict_button = (
                st.button(
                    "✨ Analyse Sentiment",
                    type="primary",
                    use_container_width=True,
                    key="predict_single_review"
                )
            )


    # --------------------------------------------------------
    # PREDICTION RESULT
    # --------------------------------------------------------

    with right_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 AI Prediction"
            )


            if predict_button:

                if not review_text.strip():

                    st.warning(
                        "Please enter a review "
                        "before analysing."
                    )

                else:

                    with st.spinner(
                        "DistilBERT is analysing "
                        "the review..."
                    ):

                        try:

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
                                    "The review indicates "
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
                                f"{confidence:.2f}%"
                            )


                            st.caption(
                                "Confidence represents "
                                "the model's output "
                                "probability and does not "
                                "guarantee prediction "
                                "correctness."
                            )


                        except Exception as error:

                            st.error(
                                "The prediction could "
                                "not be completed."
                            )

                            st.exception(
                                error
                            )


            else:

                st.info(
                    "Enter a customer review "
                    "and select Analyse Sentiment."
                )


# ============================================================
# TAB 2
# BATCH INTELLIGENCE
# ============================================================

with batch_tab:

    st.markdown(
        "## Batch Brand Intelligence"
    )

    st.caption(
        "Upload CSV or Excel review data "
        "for large-scale sentiment and "
        "brand reputation analysis."
    )


    upload_column, information_column = (
        st.columns(
            [1.7, 1],
            gap="large"
        )
    )


    # --------------------------------------------------------
    # FILE UPLOAD
    # --------------------------------------------------------

    with upload_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📂 Upload Review Dataset"
            )

            uploaded_file = (
                st.file_uploader(
                    "Upload review dataset",
                    type=[
                        "csv",
                        "xlsx"
                    ],
                    label_visibility="collapsed"
                )
            )

            st.caption(
                "Supported formats: CSV and XLSX"
            )


    # --------------------------------------------------------
    # DATA FORMAT INFORMATION
    # --------------------------------------------------------

    with information_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📌 Required Data"
            )

            st.write(
                "Your file needs at least "
                "one column containing "
                "customer review text."
            )

            st.code(
                "review_text\n"
                "Spotify is excellent...\n"
                "The app keeps crashing...",
                language=None
            )


    # --------------------------------------------------------
    # PROCESS UPLOADED FILE
    # --------------------------------------------------------

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

            st.markdown(
                "### Dataset Preview"
            )


            preview_column, stats_column = (
                st.columns(
                    [3, 1],
                    gap="medium"
                )
            )


            # ------------------------------------------------
            # DATA PREVIEW
            # ------------------------------------------------

            with preview_column:

                st.dataframe(
                    uploaded_df.head(10),
                    use_container_width=True,
                    hide_index=True
                )


            # ------------------------------------------------
            # DATASET INFORMATION
            # ------------------------------------------------

            with stats_column:

                st.metric(
                    "Total Rows",
                    f"{len(uploaded_df):,}"
                )

                st.metric(
                    "Columns",
                    len(
                        uploaded_df.columns
                    )
                )


            # ------------------------------------------------
            # REVIEW COLUMN SELECTION
            # ------------------------------------------------

            review_column = (
                st.selectbox(
                    "Select the column "
                    "containing review text:",
                    options=(
                        uploaded_df
                        .columns
                        .tolist()
                    )
                )
            )


            # ------------------------------------------------
            # CLEAN VALID REVIEWS
            # ------------------------------------------------

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
                "Valid Reviews Ready",
                f"{len(valid_reviews):,}"
            )


            # ------------------------------------------------
            # RUN ANALYSIS
            # ------------------------------------------------

            if st.button(
                "🚀 Run Brand Intelligence Analysis",
                type="primary",
                use_container_width=True,
                key="run_batch_analysis"
            ):

                if (
                    len(valid_reviews)
                    == 0
                ):

                    st.warning(
                        "No valid reviews "
                        "were found."
                    )

                else:

                    with st.status(
                        "Running AI analysis...",
                        expanded=True
                    ) as status:

                        try:

                            # --------------------------------
                            # STEP 1
                            # DISTILBERT
                            # --------------------------------

                            st.write(
                                "🧠 Running DistilBERT "
                                "sentiment predictions..."
                            )


                            prediction_list = (
                                predict_batch(
                                    valid_reviews.tolist(),
                                    batch_size=16
                                )
                            )


                            # --------------------------------
                            # STEP 2
                            # CREATE DATAFRAME
                            # --------------------------------

                            prediction_df = (
                                pd.DataFrame(
                                    prediction_list
                                )
                            )


                            st.write(
                                "📊 Calculating brand "
                                "reputation indicators..."
                            )


                            # --------------------------------
                            # STEP 3
                            # ANALYSIS
                            # --------------------------------

                            (
                                analysed_df,
                                summary
                            ) = (
                                analyse_predictions(
                                    prediction_df
                                )
                            )


                            st.write(
                                "🔎 Identifying recurring "
                                "customer issues..."
                            )


                            # --------------------------------
                            # SAVE SESSION RESULTS
                            # --------------------------------

                            st.session_state[
                                "prediction_results"
                            ] = analysed_df


                            st.session_state[
                                "analysis_summary"
                            ] = summary


                            status.update(
                                label=(
                                    "Brand intelligence "
                                    "analysis complete!"
                                ),
                                state="complete",
                                expanded=False
                            )


                        except Exception as error:

                            status.update(
                                label="Analysis failed",
                                state="error",
                                expanded=True
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
    # DISPLAY RESULTS
    # --------------------------------------------------------

    if (
        st.session_state[
            "prediction_results"
        ]
        is not None
    ):

        st.divider()

        st.markdown(
            "## Prediction Intelligence"
        )


        results_df = (
            st.session_state[
                "prediction_results"
            ].copy()
        )


        # ----------------------------------------------------
        # CONVERT CONFIDENCE TO %
        # ----------------------------------------------------

        display_results = (
            results_df.copy()
        )


        display_results[
            "confidence"
        ] = (
            display_results[
                "confidence"
            ]
            * 100
        ).round(2)


        # ----------------------------------------------------
        # FRIENDLY COLUMN NAMES
        # ----------------------------------------------------

        display_results.rename(
            columns={
                "review_text":
                    "Review",

                "predicted_sentiment":
                    "Sentiment",

                "confidence":
                    "Confidence (%)",

                "issues":
                    "Detected Issues"
            },
            inplace=True
        )


        # ----------------------------------------------------
        # RESULT TABLE
        # ----------------------------------------------------

        st.dataframe(
            display_results,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        csv_data = (
            display_results
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            label=(
                "⬇️ Download Analysis Results"
            ),
            data=csv_data,
            file_name=(
                "spotify_brand_"
                "reputation_analysis.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# TAB 3
# BRAND REPUTATION DASHBOARD
# ============================================================

with dashboard_tab:

    st.markdown(
        "## Brand Reputation Intelligence"
    )

    st.caption(
        "Executive-level brand reputation "
        "overview derived from DistilBERT "
        "review predictions."
    )


    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )


    # --------------------------------------------------------
    # NO ANALYSIS YET
    # --------------------------------------------------------

    if summary is None:

        with st.container(
            border=True
        ):

            st.info(
                "📂 Run Batch Intelligence "
                "first to generate the "
                "reputation dashboard."
            )


    else:

        # ====================================================
        # KPI SECTION
        # ====================================================

        (
            metric1,
            metric2,
            metric3,
            metric4
        ) = st.columns(
            4,
            gap="medium"
        )


        metric1.metric(
            "Reviews Analysed",
            f"{summary['total_reviews']:,}"
        )


        metric2.metric(
            "Positive Reviews",
            f"{summary['positive_reviews']:,}"
        )


        metric3.metric(
            "Negative Reviews",
            f"{summary['negative_reviews']:,}"
        )


        metric4.metric(
            "Brand Reputation Score",
            f"{summary['reputation_score']}%"
        )


        st.write("")


        # ====================================================
        # REPUTATION STATUS
        # ====================================================

        score = float(
            summary[
                "reputation_score"
            ]
        )


        with st.container(
            border=True
        ):

            st.markdown(
                "### 🧭 Reputation Status"
            )


            if score >= 80:

                st.html(
                    """
<div class="reputation-positive">
    🟢 Very Positive Brand Reputation
</div>
"""
                )


            elif score >= 60:

                st.html(
                    """
<div class="reputation-positive">
    🟢 Positive Brand Reputation
</div>
"""
                )


            elif score >= 40:

                st.html(
                    """
<div class="reputation-mixed">
    🟡 Mixed Brand Reputation
</div>
"""
                )


            elif score >= 20:

                st.html(
                    """
<div class="reputation-negative">
    🔴 Negative Brand Reputation
</div>
"""
                )


            else:

                st.html(
                    """
<div class="reputation-negative">
    🔴 Very Negative Brand Reputation
</div>
"""
                )


            st.write("")


            st.progress(
                int(
                    max(
                        0,
                        min(
                            100,
                            score
                        )
                    )
                )
            )


            st.caption(
                f"Current Reputation Score: "
                f"{score:.2f}%"
            )


        st.write("")


        # ====================================================
        # CHART SECTION
        # ====================================================

        chart_left, chart_right = (
            st.columns(
                2,
                gap="large"
            )
        )


        # ----------------------------------------------------
        # SENTIMENT CHART
        # ----------------------------------------------------

        with chart_left:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Sentiment Distribution"
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


                sentiment_chart = (
                    px.pie(
                        sentiment_df,
                        names="Sentiment",
                        values="Reviews",
                        hole=0.62
                    )
                )


                sentiment_chart.update_layout(
                    margin=dict(
                        l=10,
                        r=10,
                        t=20,
                        b=10
                    ),

                    legend_title_text=""
                )


                st.plotly_chart(
                    sentiment_chart,
                    use_container_width=True
                )


        # ----------------------------------------------------
        # ISSUE CHART
        # ----------------------------------------------------

        with chart_right:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Main Reputation Issues"
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
                                        count
                                }

                                for (
                                    issue,
                                    count
                                )
                                in issue_counts.items()
                            ]
                        )
                    )


                    issue_df = (
                        issue_df
                        .sort_values(
                            "Mentions",
                            ascending=True
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


                    issue_chart.update_layout(
                        margin=dict(
                            l=10,
                            r=10,
                            t=20,
                            b=10
                        )
                    )


                    st.plotly_chart(
                        issue_chart,
                        use_container_width=True
                    )


                else:

                    st.info(
                        "No issue categories "
                        "were detected."
                    )


        # ====================================================
        # CUSTOMER VOICE
        # ====================================================

        st.markdown(
            "## Customer Voice Intelligence"
        )


        positive_words_column, negative_words_column = (
            st.columns(
                2,
                gap="large"
            )
        )


        # ----------------------------------------------------
        # POSITIVE WORDS
        # ----------------------------------------------------

        with positive_words_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 💚 Positive Customer Voice"
                )


                positive_words_df = (
                    pd.DataFrame(
                        summary[
                            "top_positive_words"
                        ]
                    )
                )


                if not positive_words_df.empty:

                    positive_words_df.rename(
                        columns={
                            "word": "Word",
                            "count": "Frequency"
                        },
                        inplace=True
                    )


                    st.dataframe(
                        positive_words_df,
                        use_container_width=True,
                        hide_index=True
                    )


                else:

                    st.info(
                        "No positive words available."
                    )


        # ----------------------------------------------------
        # NEGATIVE WORDS
        # ----------------------------------------------------

        with negative_words_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🚨 Negative Customer Voice"
                )


                negative_words_df = (
                    pd.DataFrame(
                        summary[
                            "top_negative_words"
                        ]
                    )
                )


                if not negative_words_df.empty:

                    negative_words_df.rename(
                        columns={
                            "word": "Word",
                            "count": "Frequency"
                        },
                        inplace=True
                    )


                    st.dataframe(
                        negative_words_df,
                        use_container_width=True,
                        hide_index=True
                    )


                else:

                    st.info(
                        "No negative words available."
                    )


        # ====================================================
        # REVIEWS REQUIRING ATTENTION
        # ====================================================

        st.markdown(
            "## Reviews Requiring Attention"
        )


        with st.container(
            border=True
        ):

            negative_reviews = (
                summary[
                    "sample_negative_reviews"
                ]
            )


            if negative_reviews:

                for (
                    index,
                    review
                ) in enumerate(
                    negative_reviews,
                    start=1
                ):

                    with st.expander(
                        f"⚠️ Customer Issue {index}"
                    ):

                        st.write(
                            review
                        )


            else:

                st.success(
                    "No negative reviews "
                    "were detected."
                )


        # ====================================================
        # METHODOLOGY NOTE
        # ====================================================

        st.info(
            "The Brand Reputation Score is a "
            "project-defined indicator calculated "
            "from the proportion of positive "
            "DistilBERT predictions. It should "
            "not be interpreted as a universal "
            "industry-standard reputation metric."
        )

        # ============================================================
# DEVELOPER TEST
# GEMINI + OPENROUTER
# TEMPORARY SECTION
# ============================================================

st.divider()

st.markdown(
    "## 🧪 LLM Connection Test"
)

st.caption(
    "Temporary developer section used to verify "
    "Gemini and OpenRouter connectivity before "
    "building the AI Management Council."
)


# ============================================================
# TEST INFORMATION
# ============================================================

with st.container(
    border=True
):

    st.markdown(
        "### Connected LLM Services"
    )

    provider_col1, provider_col2 = (
        st.columns(2)
    )


    with provider_col1:

        st.markdown(
            "#### ✨ Gemini"
        )

        st.write(
            "Provider: Google Gemini API"
        )

        st.write(
            "Configured model:"
        )

        st.code(
            st.secrets.get(
                "GEMINI_MODEL",
                "Not configured"
            ),
            language=None
        )


    with provider_col2:

        st.markdown(
            "#### 🌐 OpenRouter"
        )

        st.write(
            "Provider: OpenRouter"
        )

        st.write(
            "Requested model/router:"
        )

        st.code(
            st.secrets.get(
                "OPENROUTER_MODEL",
                "Not configured"
            ),
            language=None
        )


st.write("")


# ============================================================
# TEST PROMPT
# ============================================================

with st.container(
    border=True
):

    st.markdown(
        "### 📝 Test Prompt"
    )

    test_prompt = st.text_area(
        "Enter a test message",
        value=(
            "Reply with a short sentence confirming "
            "that the API connection is working."
        ),
        height=100
    )

    test_button = st.button(
        "🚀 Test Gemini + OpenRouter",
        type="primary",
        use_container_width=True,
        key="test_both_llm_connections"
    )


# ============================================================
# RUN BOTH TESTS
# ============================================================

if test_button:

    if not test_prompt.strip():

        st.warning(
            "Please enter a test prompt."
        )

    else:

        st.markdown(
            "## Test Results"
        )

        gemini_column, openrouter_column = (
            st.columns(
                2,
                gap="large"
            )
        )


        # ====================================================
        # GEMINI TEST
        # ====================================================

        with gemini_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### ✨ Gemini"
                )

                try:

                    with st.spinner(
                        "Connecting to Gemini..."
                    ):

                        gemini_result = (
                            call_gemini(
                                system_prompt=(
                                    "You are a connection-test "
                                    "assistant. Respond clearly "
                                    "and briefly."
                                ),

                                user_prompt=(
                                    test_prompt
                                )
                            )
                        )


                    st.success(
                        "Gemini connection successful!"
                    )


                    st.markdown(
                        "#### Response"
                    )

                    st.write(
                        gemini_result[
                            "content"
                        ]
                    )


                    st.divider()


                    info_col1, info_col2 = (
                        st.columns(2)
                    )


                    info_col1.metric(
                        "Provider",
                        gemini_result[
                            "provider"
                        ]
                    )


                    info_col2.metric(
                        "Model",
                        gemini_result[
                            "model"
                        ]
                    )


                except Exception as error:

                    st.error(
                        "Gemini connection failed."
                    )

                    st.exception(
                        error
                    )


        # ====================================================
        # OPENROUTER TEST
        # ====================================================

        with openrouter_column:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🌐 OpenRouter Free"
                )

                try:

                    with st.spinner(
                        "Connecting to OpenRouter..."
                    ):

                        openrouter_result = (
                            call_openrouter(
                                system_prompt=(
                                    "You are a connection-test "
                                    "assistant. Respond clearly "
                                    "and briefly."
                                ),

                                user_prompt=(
                                    test_prompt
                                )
                            )
                        )


                    st.success(
                        "OpenRouter connection successful!"
                    )


                    st.markdown(
                        "#### Response"
                    )

                    st.write(
                        openrouter_result[
                            "content"
                        ]
                    )


                    st.divider()


                    info_col1, info_col2 = (
                        st.columns(2)
                    )


                    info_col1.metric(
                        "Provider",
                        openrouter_result[
                            "provider"
                        ]
                    )


                    info_col2.metric(
                        "Actual Model",
                        openrouter_result[
                            "model"
                        ]
                    )


                    st.caption(
                        "The actual OpenRouter model may "
                        "change because the application "
                        "requests openrouter/free."
                    )


                except Exception as error:

                    st.error(
                        "OpenRouter connection failed."
                    )

                    st.exception(
                        error
                    )


        # ====================================================
        # FINAL CONNECTION SUMMARY
        # ====================================================

        st.write("")

        st.info(
            "If both panels show a successful connection, "
            "the LLM service layer is ready for the "
            "AI Management Council."
        )
