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

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Hero */
    .hero {
        padding: 32px 36px;
        border-radius: 24px;
        margin-bottom: 24px;

        background:
            radial-gradient(
                circle at top right,
                rgba(29, 185, 84, 0.28),
                transparent 35%
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
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;

        border-radius: 999px;

        background:
            rgba(29, 185, 84, 0.13);

        color: #55E487;

        font-size: 13px;
        font-weight: 600;

        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin: 0;
        line-height: 1.05;
    }

    .hero-subtitle {
        color: #A9B1BC;
        font-size: 16px;

        max-width: 850px;

        margin-top: 14px;
        margin-bottom: 0;
    }

    /* Section heading */
    .section-label {
        color: #8F99A8;
        font-size: 12px;

        font-weight: 700;
        letter-spacing: 1.3px;

        text-transform: uppercase;

        margin-bottom: 3px;
    }

    /* Status pill */
    .status-online {
        display: inline-block;

        padding: 5px 10px;

        border-radius: 999px;

        color: #55E487;

        background:
            rgba(29, 185, 84, 0.12);

        font-size: 12px;
        font-weight: 600;
    }

    /* Feature card */
    .feature-card {
        padding: 20px;

        border-radius: 18px;

        background: #171B22;

        border:
            1px solid rgba(
                255,
                255,
                255,
                0.07
            );

        min-height: 145px;
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .feature-text {
        color: #9CA6B3;
        font-size: 13px;
        line-height: 1.5;
    }

    /* Small hint */
    .hint-text {
        color: #8993A0;
        font-size: 13px;
    }

    /* Remove excessive top whitespace */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_results" not in st.session_state:
    st.session_state.prediction_results = None

if "analysis_summary" not in st.session_state:
    st.session_state.analysis_summary = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎧 BrandPulse AI")

    st.caption(
        "AI-Assisted Brand Reputation "
        "Decision-Support System"
    )

    st.divider()

    st.markdown(
        '<div class="section-label">'
        'DEPLOYMENT MODEL'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### DistilBERT")

    st.caption(
        "Binary sentiment classification"
    )

    st.markdown(
        '<span class="status-online">'
        '● Model Online'
        '</span>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-label">'
        'CLASSIFICATION'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("🟢 Positive")
    st.write("🔴 Negative")

    st.divider()

    st.markdown(
        '<div class="section-label">'
        'SYSTEM PIPELINE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        **1.** Upload reviews  
        **2.** DistilBERT prediction  
        **3.** Reputation analysis  
        **4.** Issue detection  
        **5.** Management intelligence
        """
    )

    st.divider()

    st.caption(
        "Final Year Project • "
        "Online Review-Based Brand "
        "Reputation Prediction"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            AI BRAND INTELLIGENCE
        </div>

        <div class="hero-title">
            BrandPulse AI
        </div>

        <p class="hero-subtitle">
            Transform Spotify customer reviews into
            actionable brand reputation intelligence
            using DistilBERT sentiment classification,
            issue analysis and AI-assisted management
            insights.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK FEATURE CARDS
# ============================================================

feature1, feature2, feature3, feature4 = st.columns(4)

with feature1:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">
                DistilBERT AI
            </div>
            <div class="feature-text">
                Transformer-based sentiment
                classification for Spotify reviews.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature2:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">
                Reputation Analytics
            </div>
            <div class="feature-text">
                Convert sentiment predictions into
                measurable brand reputation insights.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature3:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔎</div>
            <div class="feature-title">
                Issue Intelligence
            </div>
            <div class="feature-text">
                Identify recurring technical,
                subscription and customer issues.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature4:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">
                AI Management
            </div>
            <div class="feature-text">
                Department-level recommendations
                will be generated by LLM managers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# MAIN NAVIGATION
# ============================================================

single_tab, batch_tab, dashboard_tab = st.tabs(
    [
        "🧪 Single Review",
        "📂 Batch Intelligence",
        "📈 Reputation Dashboard"
    ]
)


# ============================================================
# SINGLE REVIEW
# ============================================================

with single_tab:

    st.markdown("## Review Sentiment Laboratory")

    st.caption(
        "Test your deployed DistilBERT model "
        "with an individual Spotify review."
    )

    left, right = st.columns(
        [1.5, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with left:

        with st.container(
            border=True
        ):

            st.markdown(
                "### ✍️ Customer Review"
            )

            review_text = st.text_area(
                "Review text",
                placeholder=(
                    "Example: Spotify keeps crashing "
                    "after the latest update and "
                    "playback randomly stops."
                ),
                height=190,
                label_visibility="collapsed"
            )

            st.markdown(
                '<span class="hint-text">'
                'Enter an English-language Spotify review.'
                '</span>',
                unsafe_allow_html=True
            )

            st.write("")

            predict_button = st.button(
                "✨ Analyse Sentiment",
                type="primary",
                width="stretch"
            )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with right:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 AI Prediction"
            )

            if predict_button:

                if not review_text.strip():

                    st.warning(
                        "Enter a review before analysing."
                    )

                else:

                    with st.spinner(
                        "DistilBERT is analysing "
                        "the review..."
                    ):

                        try:

                            result = predict_sentiment(
                                review_text
                            )

                            sentiment = (
                                result["sentiment"]
                                .lower()
                            )

                            confidence = (
                                result["confidence"]
                                * 100
                            )

                            if sentiment == "positive":

                                st.success(
                                    "### 🟢 Positive"
                                )

                                st.write(
                                    "The review reflects "
                                    "a favourable customer "
                                    "experience."
                                )

                            elif sentiment == "negative":

                                st.error(
                                    "### 🔴 Negative"
                                )

                                st.write(
                                    "The review indicates "
                                    "customer dissatisfaction."
                                )

                            else:

                                st.info(
                                    sentiment.title()
                                )

                            st.metric(
                                "Model Confidence",
                                f"{confidence:.2f}%",
                                border=True
                            )

                        except Exception as error:

                            st.error(
                                "Prediction could not "
                                "be completed."
                            )

                            st.exception(error)

            else:

                st.info(
                    "Your sentiment prediction "
                    "will appear here."
                )


# ============================================================
# BATCH ANALYSIS
# ============================================================

with batch_tab:

    st.markdown(
        "## Batch Brand Intelligence"
    )

    st.caption(
        "Analyse multiple Spotify reviews "
        "from CSV or Excel."
    )


    upload_column, information_column = (
        st.columns(
            [1.7, 1],
            gap="large"
        )
    )


    # --------------------------------------------------------
    # UPLOAD AREA
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
                    "Upload dataset",
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
    # INFORMATION
    # --------------------------------------------------------

    with information_column:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📌 Required Data"
            )

            st.write(
                "Your file only needs one "
                "column containing customer "
                "review text."
            )

            st.code(
                "review_text\n"
                "Spotify is excellent...\n"
                "The app keeps crashing...",
                language=None
            )


    if uploaded_file is not None:

        try:

            if (
                uploaded_file.name
                .lower()
                .endswith(".csv")
            ):

                uploaded_df = pd.read_csv(
                    uploaded_file
                )

            else:

                uploaded_df = pd.read_excel(
                    uploaded_file
                )


            st.write("")

            st.markdown(
                "### Dataset Preview"
            )

            preview_col1, preview_col2 = (
                st.columns(
                    [3, 1]
                )
            )


            with preview_col1:

                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True
                )


            with preview_col2:

                st.metric(
                    "Total Rows",
                    f"{len(uploaded_df):,}",
                    border=True
                )

                st.metric(
                    "Columns",
                    len(
                        uploaded_df.columns
                    ),
                    border=True
                )


            review_column = st.selectbox(
                "Select review-text column",
                uploaded_df.columns.tolist()
            )


            valid_reviews = (
                uploaded_df[
                    review_column
                ]
                .dropna()
                .astype(str)
                .str.strip()
            )

            valid_reviews = valid_reviews[
                valid_reviews != ""
            ]


            st.metric(
                "Valid Reviews Ready for Analysis",
                f"{len(valid_reviews):,}",
                border=True
            )


            if st.button(
                "🚀 Run Brand Intelligence Analysis",
                type="primary",
                width="stretch"
            ):

                if len(valid_reviews) == 0:

                    st.warning(
                        "No valid reviews found."
                    )

                else:

                    with st.status(
                        "Running AI analysis...",
                        expanded=True
                    ) as status:

                        try:

                            st.write(
                                "🧠 Running "
                                "DistilBERT predictions..."
                            )

                            prediction_list = (
                                predict_batch(
                                    valid_reviews.tolist(),
                                    batch_size=16
                                )
                            )

                            st.write(
                                "📊 Calculating "
                                "reputation indicators..."
                            )

                            prediction_df = (
                                pd.DataFrame(
                                    prediction_list
                                )
                            )

                            (
                                analysed_df,
                                summary
                            ) = analyse_predictions(
                                prediction_df
                            )

                            st.write(
                                "🔎 Identifying "
                                "customer issues..."
                            )


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
                                label=(
                                    "Analysis failed"
                                ),
                                state="error"
                            )

                            st.exception(
                                error
                            )


        except Exception as error:

            st.error(
                "Unable to read the uploaded file."
            )

            st.exception(error)


    # --------------------------------------------------------
    # RESULTS TABLE
    # --------------------------------------------------------

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

        st.divider()

        st.markdown(
            "## Prediction Intelligence"
        )


        display_results = (
            results.copy()
        )

        display_results[
            "confidence"
        ] = (
            display_results[
                "confidence"
            ]
            * 100
        ).round(2)


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


        st.dataframe(
            display_results,
            width="stretch",
            hide_index=True
        )


        download_data = (
            display_results
            .to_csv(
                index=False
            )
            .encode("utf-8")
        )


        st.download_button(
            "⬇️ Download Analysis Results",
            data=download_data,
            file_name=(
                "spotify_brand_"
                "reputation_analysis.csv"
            ),
            mime="text/csv",
            width="stretch"
        )


# ============================================================
# REPUTATION DASHBOARD
# ============================================================

with dashboard_tab:

    st.markdown(
        "## Brand Reputation Intelligence"
    )

    st.caption(
        "Executive overview derived from "
        "DistilBERT review predictions."
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
                "📂 Run a Batch Intelligence "
                "analysis first to generate "
                "the dashboard."
            )


    else:

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )


        metric1.metric(
            "Reviews Analysed",
            f"{summary['total_reviews']:,}",
            border=True
        )


        metric2.metric(
            "Positive Reviews",
            f"{summary['positive_reviews']:,}",
            border=True
        )


        metric3.metric(
            "Negative Reviews",
            f"{summary['negative_reviews']:,}",
            border=True
        )


        metric4.metric(
            "Brand Reputation Score",
            f"{summary['reputation_score']}%",
            border=True
        )


        st.write("")


        # ----------------------------------------------------
        # REPUTATION STATUS
        # ----------------------------------------------------

        score = summary[
            "reputation_score"
        ]


        with st.container(
            border=True
        ):

            st.markdown(
                "### 🧭 Reputation Status"
            )


            if score >= 80:

                st.success(
                    "Very Positive Brand Reputation"
                )

            elif score >= 60:

                st.success(
                    "Positive Brand Reputation"
                )

            elif score >= 40:

                st.warning(
                    "Mixed Brand Reputation"
                )

            elif score >= 20:

                st.error(
                    "Negative Brand Reputation"
                )

            else:

                st.error(
                    "Very Negative Brand Reputation"
                )


            st.progress(
                int(score)
            )


        st.write("")


        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        chart_left, chart_right = (
            st.columns(
                2,
                gap="large"
            )
        )


        with chart_left:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Sentiment Distribution"
                )


                sentiment_df = pd.DataFrame(
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


                sentiment_chart = px.pie(
                    sentiment_df,
                    names="Sentiment",
                    values="Reviews",
                    hole=0.62
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
                    width="stretch"
                )


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

                    issue_df = pd.DataFrame(
                        [
                            {
                                "Issue":
                                    issue,

                                "Mentions":
                                    count
                            }

                            for issue, count
                            in issue_counts.items()
                        ]
                    )


                    issue_df = (
                        issue_df
                        .sort_values(
                            "Mentions",
                            ascending=True
                        )
                    )


                    issue_chart = px.bar(
                        issue_df,
                        x="Mentions",
                        y="Issue",
                        orientation="h"
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
                        width="stretch"
                    )

                else:

                    st.info(
                        "No issue categories found."
                    )


        # ----------------------------------------------------
        # WORD INTELLIGENCE
        # ----------------------------------------------------

        st.markdown(
            "## Customer Voice Intelligence"
        )


        words1, words2 = st.columns(
            2,
            gap="large"
        )


        with words1:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 💚 Positive Customer Voice"
                )

                positive_df = pd.DataFrame(
                    summary[
                        "top_positive_words"
                    ]
                )

                st.dataframe(
                    positive_df,
                    width="stretch",
                    hide_index=True
                )


        with words2:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🚨 Negative Customer Voice"
                )

                negative_df = pd.DataFrame(
                    summary[
                        "top_negative_words"
                    ]
                )

                st.dataframe(
                    negative_df,
                    width="stretch",
                    hide_index=True
                )


        # ----------------------------------------------------
        # NEGATIVE REVIEWS
        # ----------------------------------------------------

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

                for index, review in enumerate(
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


        st.caption(
            "Brand Reputation Score is a "
            "project-defined indicator based "
            "on the proportion of positive "
            "DistilBERT classifications."
        )
