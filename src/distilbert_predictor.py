import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


MAX_LENGTH = 96


@st.cache_resource
def load_distilbert_model():
    """
    Load the final DistilBERT model from
    Hugging Face only once per Streamlit session.
    """

    model_repository = st.secrets[
        "HF_MODEL_REPO"
    ]

    hf_token = st.secrets[
        "HF_TOKEN"
    ]

    tokenizer = (
        AutoTokenizer.from_pretrained(
            model_repository,
            token=hf_token
        )
    )

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            model_repository,
            token=hf_token
        )
    )

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model.to(device)
    model.eval()

    return tokenizer, model, device


def predict_sentiment(text):
    """
    Predict a single review.
    """

    results = predict_batch(
        [str(text)],
        batch_size=1
    )

    return results[0]


def predict_batch(
    reviews,
    batch_size=16
):
    """
    Predict multiple Spotify reviews
    using DistilBERT in batches.
    """

    tokenizer, model, device = (
        load_distilbert_model()
    )

    all_results = []

    total_reviews = len(reviews)

    for start_index in range(
        0,
        total_reviews,
        batch_size
    ):

        batch_reviews = reviews[
            start_index:
            start_index + batch_size
        ]

        inputs = tokenizer(
            batch_reviews,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH
        )

        inputs = {
            key: value.to(device)
            for key, value
            in inputs.items()
        }

        with torch.no_grad():

            outputs = model(
                **inputs
            )

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        predicted_ids = (
            probabilities.argmax(
                dim=-1
            )
        )

        confidence_values = (
            probabilities.max(
                dim=-1
            ).values
        )

        for (
            review,
            predicted_id,
            confidence
        ) in zip(
            batch_reviews,
            predicted_ids,
            confidence_values
        ):

            label_id = int(
                predicted_id.item()
            )

            sentiment = (
                model.config.id2label[
                    label_id
                ]
            )

            all_results.append({
                "review_text": review,
                "predicted_sentiment": (
                    sentiment.lower()
                ),
                "confidence": float(
                    confidence.item()
                )
            })

    return all_results
