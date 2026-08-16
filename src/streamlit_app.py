import streamlit as st

from src.distilbert_predictor import (
    predict_sentiment
)


st.set_page_config(
    page_title=(
        "Spotify Brand Reputation Analysis"
    ),
    page_icon="📊",
    layout="wide"
)


st.title(
    "Spotify Brand Reputation Analysis"
)

st.write(
    "Online Review-Based Brand Reputation "
    "Prediction Using NLP Techniques"
)


st.subheader(
    "DistilBERT Sentiment Prediction"
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
    type="primary"
):

    if not review_text.strip():

        st.warning(
            "Please enter a review first."
        )

    else:

        with st.spinner(
            "Analysing review..."
        ):

            try:

                result = predict_sentiment(
                    review_text
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

                st.subheader(
                    "Prediction Result"
                )

                if sentiment == "positive":

                    st.success(
                        "Predicted Sentiment: "
                        "Positive"
                    )

                elif sentiment == "negative":

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
                    "The DistilBERT model "
                    "could not be loaded or "
                    "used for prediction."
                )

                st.exception(
                    error
                )
