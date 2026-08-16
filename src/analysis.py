from collections import Counter
import re

import pandas as pd


ISSUE_CATEGORIES = {

    "Technical Performance": [
        "crash",
        "crashing",
        "bug",
        "bugs",
        "freeze",
        "freezing",
        "lag",
        "lagging",
        "slow",
        "error",
        "glitch"
    ],

    "Playback": [
        "playback",
        "buffer",
        "buffering",
        "audio",
        "song stops",
        "music stops",
        "pause",
        "skip",
        "offline"
    ],

    "Subscription and Pricing": [
        "premium",
        "price",
        "pricing",
        "expensive",
        "payment",
        "billing",
        "subscription",
        "charged"
    ],

    "Advertisements": [
        "advertisement",
        "advertisements",
        "advertising",
        "ads"
    ],

    "Account and Login": [
        "login",
        "log in",
        "sign in",
        "password",
        "account"
    ],

    "Playlist and Library": [
        "playlist",
        "playlists",
        "library",
        "liked songs",
        "saved songs",
        "queue"
    ],

    "User Interface": [
        "interface",
        "navigation",
        "layout",
        "design",
        "button",
        "menu"
    ],

    "Customer Service": [
        "support",
        "customer service",
        "refund",
        "help",
        "response"
    ]
}


STOP_WORDS = {

    "the",
    "and",
    "this",
    "that",
    "with",
    "for",
    "you",
    "your",
    "have",
    "has",
    "was",
    "were",
    "are",
    "but",
    "not",
    "app",
    "spotify",
    "from",
    "they",
    "their",
    "its",
    "very",
    "really"
}


def identify_issues(text):
    """
    Identify issue categories from one review.

    A review may contain more than one issue.
    """

    text = str(text).lower()

    identified_categories = []

    for (
        category,
        keywords
    ) in ISSUE_CATEGORIES.items():

        found = any(
            keyword in text
            for keyword in keywords
        )

        if found:

            identified_categories.append(
                category
            )

    if not identified_categories:

        identified_categories.append(
            "Other or Unclear"
        )

    return identified_categories


def extract_top_words(
    texts,
    limit=15
):
    """
    Extract frequent words from a collection
    of reviews.
    """

    word_counter = Counter()

    for text in texts:

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            str(text).lower()
        )

        filtered_words = [

            word

            for word in words

            if word not in STOP_WORDS
        ]

        word_counter.update(
            filtered_words
        )

    return [

        {
            "word": word,
            "count": count
        }

        for word, count
        in word_counter.most_common(
            limit
        )
    ]


def analyse_predictions(
    prediction_df
):
    """
    Convert DistilBERT predictions into
    brand reputation analysis.
    """

    df = prediction_df.copy()

    df[
        "predicted_sentiment"
    ] = (
        df[
            "predicted_sentiment"
        ]
        .astype(str)
        .str.lower()
    )

    positive_mask = (
        df[
            "predicted_sentiment"
        ]
        == "positive"
    )

    negative_mask = (
        df[
            "predicted_sentiment"
        ]
        == "negative"
    )

    positive_count = int(
        positive_mask.sum()
    )

    negative_count = int(
        negative_mask.sum()
    )

    total_classified = (
        positive_count
        + negative_count
    )

    if total_classified > 0:

        reputation_score = (
            positive_count
            / total_classified
            * 100
        )

    else:

        reputation_score = 0.0

    df["issues"] = (
        df["review_text"]
        .apply(
            identify_issues
        )
    )

    negative_reviews = df[
        negative_mask
    ].copy()

    issue_counter = Counter()

    for issue_list in (
        negative_reviews[
            "issues"
        ]
    ):

        issue_counter.update(
            issue_list
        )

    positive_texts = (
        df.loc[
            positive_mask,
            "review_text"
        ]
        .astype(str)
        .tolist()
    )

    negative_texts = (
        df.loc[
            negative_mask,
            "review_text"
        ]
        .astype(str)
        .tolist()
    )

    summary = {

        "total_reviews":
            int(len(df)),

        "positive_reviews":
            positive_count,

        "negative_reviews":
            negative_count,

        "positive_percentage":
            round(
                reputation_score,
                2
            ),

        "negative_percentage":
            round(
                (
                    negative_count
                    / total_classified
                    * 100
                )
                if total_classified > 0
                else 0.0,
                2
            ),

        "reputation_score":
            round(
                reputation_score,
                2
            ),

        "issue_counts":
            dict(
                issue_counter.most_common()
            ),

        "top_positive_words":
            extract_top_words(
                positive_texts
            ),

        "top_negative_words":
            extract_top_words(
                negative_texts
            ),

        "sample_negative_reviews":
            negative_texts[:10],

        "sample_positive_reviews":
            positive_texts[:5]
    }

    return df, summary
