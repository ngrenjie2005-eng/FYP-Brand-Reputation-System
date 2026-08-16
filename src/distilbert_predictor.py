import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


MAX_LENGTH = 96


@st.cache_resource
def load_distilbert_model():

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

    model.eval()

    return tokenizer, model


def predict_sentiment(text):

    tokenizer, model = (
        load_distilbert_model()
    )

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    with torch.no_grad():

        outputs = model(
            **inputs
        )

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )

    predicted_id = int(
        probabilities.argmax(
            dim=-1
        ).item()
    )

    confidence = float(
        probabilities[
            0,
            predicted_id
        ].item()
    )

    sentiment = (
        model.config.id2label[
            predicted_id
        ]
    )

    return {
        "sentiment": sentiment,
        "confidence": confidence
    }
