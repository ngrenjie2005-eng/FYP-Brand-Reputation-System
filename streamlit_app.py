import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import (
    analyse_predictions
)

from src.distilbert_predictor import (
    predict_sentiment,
    predict_batch
)


st.set_page_config(
    page_title=(
        "Spotify Brand Reputation Analysis"
    ),
    page_icon="📊",
    layout="wide"
)


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


# ============================================================
# HEADER
# ============================================================

st.title(
    "Spotify Brand Reputation Analysis"
)

st.caption(
    "Online Review-Based Brand Reputation "
    "Prediction Using NLP Techniques"
)


st.info(
    "The deployed sentiment classification "
    "model is DistilBERT."
)


# ============================================================
# TABS
# ============================================================

single_tab, batch_tab, dashboard_tab = (
    st.tabs([
        "Single Review",
        "Batch Review Analysis",
        "Brand Reputation Dashboard"
    ])
)


# ============================================================
# TAB 1 - SINGLE REVIEW
# ============================================================

with single_tab:

    st.header(
        "Single Review Prediction"
    )

    review_text = st.text_area(
        "Enter a Spotify review:",
        placeholder=(
            "Example: The app keeps crashing "
            "after the latest update."
        ),
        height=150
    )

    if st.button(
        "Predict Sentiment",
        type="primary",
        key="single_prediction"
    ):

        if not review_text.strip():

            st.warning(
                "Please enter a review."
            )

        else:

            with st.spinner(
                "Analysing review..."
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
                        ].lower()
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
                            "Predicted Sentiment: "
                            "Positive"
                        )

                    elif (
                        sentiment
                        == "negative"
                    ):

                        st.error(
                            "Predicted Sentiment: "
                            "Negative"
                        )

                    else:

                        st.info(
                            "Predicted Sentiment: "
                            f"{sentiment}"
                        )

                    st.metric(
                        "Model Confidence",
                        f"{confidence:.2f}%"
                    )

                except Exception as error:

                    st.error(
                        "Prediction failed."
                    )

                    st.exception(
                        error
                    )


# ============================================================
# TAB 2 - BATCH REVIEW ANALYSIS
# ============================================================

with batch_tab:

    st.header(
        "Batch Review Analysis"
    )

    st.write(
        "Upload a CSV or Excel file "
        "containing Spotify reviews."
    )

    uploaded_file = (
        st.file_uploader(
            "Upload review dataset",
            type=[
                "csv",
                "xlsx"
            ]
        )
    )

    if uploaded_file is not None:

        try:

            file_name = (
                uploaded_file.name.lower()
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

            st.subheader(
                "Dataset Preview"
            )

            st.dataframe(
                uploaded_df.head(10),
                use_container_width=True
            )

            st.write(
                "Rows:",
                len(uploaded_df)
            )

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

            st.write(
                "Valid reviews:",
                len(valid_reviews)
            )

            if st.button(
                "Analyse All Reviews",
                type="primary",
                key="batch_analysis"
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

                    progress_bar = (
                        st.progress(0)
                    )

                    status_text = (
                        st.empty()
                    )

                    status_text.write(
                        "Running "
                        "DistilBERT predictions..."
                    )

                    try:

                        prediction_list = (
                            predict_batch(
                                valid_reviews.tolist(),
                                batch_size=16
                            )
                        )

                        progress_bar.progress(
                            70
                        )

                        prediction_df = (
                            pd.DataFrame(
                                prediction_list
                            )
                        )

                        status_text.write(
                            "Calculating brand "
                            "reputation analysis..."
                        )

                        (
                            analysed_df,
                            summary
                        ) = (
                            analyse_predictions(
                                prediction_df
                            )
                        )

                        progress_bar.progress(
                            100
                        )

                        st.session_state[
                            "prediction_results"
                        ] = analysed_df

                        st.session_state[
                            "analysis_summary"
                        ] = summary

                        status_text.empty()
                        progress_bar.empty()

                        st.success(
                            "Review analysis "
                            "completed successfully."
                        )

                    except Exception as error:

                        progress_bar.empty()

                        status_text.empty()

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


    # Display saved results
    if (
        st.session_state[
            "prediction_results"
        ]
        is not None
    ):

        result_df = (
            st.session_state[
                "prediction_results"
            ]
        )

        st.subheader(
            "Prediction Results"
        )

        display_df = (
            result_df.copy()
        )

        display_df[
            "confidence"
        ] = (
            display_df[
                "confidence"
            ]
            * 100
        ).round(2)

        display_df.rename(
            columns={
                "confidence":
                    "confidence_percent"
            },
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True
        )

        csv_data = (
            display_df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )

        st.download_button(
            label=(
                "Download Prediction Results"
            ),
            data=csv_data,
            file_name=(
                "spotify_review_predictions.csv"
            ),
            mime="text/csv"
        )


# ============================================================
# TAB 3 - BRAND REPUTATION DASHBOARD
# ============================================================

with dashboard_tab:

    st.header(
        "Brand Reputation Dashboard"
    )

    summary = (
        st.session_state[
            "analysis_summary"
        ]
    )

    if summary is None:

        st.warning(
            "Please run Batch Review "
            "Analysis first."
        )

    else:

        # ----------------------------------------------------
        # MAIN METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(
            "Reviews Analysed",
            f"{summary['total_reviews']:,}"
        )

        col2.metric(
            "Positive Reviews",
            f"{summary['positive_reviews']:,}"
        )

        col3.metric(
            "Negative Reviews",
            f"{summary['negative_reviews']:,}"
        )

        col4.metric(
            "Reputation Score",
            (
                f"{summary['reputation_score']}"
                "%"
            )
        )


        st.divider()


        # ----------------------------------------------------
        # SENTIMENT DISTRIBUTION
        # ----------------------------------------------------

        sentiment_data = (
            pd.DataFrame({
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
            })
        )

        sentiment_figure = (
            px.pie(
                sentiment_data,
                names="Sentiment",
                values="Reviews",
                title=(
                    "Predicted Sentiment "
                    "Distribution"
                )
            )
        )

        st.plotly_chart(
            sentiment_figure,
            use_container_width=True
        )


        # ----------------------------------------------------
        # ISSUE CATEGORIES
        # ----------------------------------------------------

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
                            "Issue Category":
                                category,

                            "Mentions":
                                count
                        }

                        for (
                            category,
                            count
                        )
                        in issue_counts.items()
                    ]
                )
            )

            issue_df = (
                issue_df.sort_values(
                    "Mentions",
                    ascending=True
                )
            )

            issue_figure = (
                px.bar(
                    issue_df,
                    x="Mentions",
                    y="Issue Category",
                    orientation="h",
                    title=(
                        "Issue Mentions in "
                        "Negative Reviews"
                    )
                )
            )

            st.plotly_chart(
                issue_figure,
                use_container_width=True
            )


        # ----------------------------------------------------
        # FREQUENT WORDS
        # ----------------------------------------------------

        positive_column, negative_column = (
            st.columns(2)
        )


        with positive_column:

            st.subheader(
                "Frequent Positive Words"
            )

            positive_words_df = (
                pd.DataFrame(
                    summary[
                        "top_positive_words"
                    ]
                )
            )

            st.dataframe(
                positive_words_df,
                use_container_width=True
            )


        with negative_column:

            st.subheader(
                "Frequent Negative Words"
            )

            negative_words_df = (
                pd.DataFrame(
                    summary[
                        "top_negative_words"
                    ]
                )
            )

            st.dataframe(
                negative_words_df,
                use_container_width=True
            )


        # ----------------------------------------------------
        # SAMPLE NEGATIVE REVIEWS
        # ----------------------------------------------------

        st.subheader(
            "Sample Negative Reviews"
        )

        for review in (
            summary[
                "sample_negative_reviews"
            ]
        ):

            st.markdown(
                f"- {review}"
            )


        st.info(
            "The Brand Reputation Score "
            "is a project-defined indicator "
            "based on the proportion of "
            "positive DistilBERT predictions. "
            "It is not a universal "
            "industry-standard reputation score."
        )
