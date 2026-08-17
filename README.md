# 🎧 BrandPulse AI

## Online Review-Based Brand Reputation Prediction Using NLP Techniques

**BrandPulse AI** is a Final Year Project (FYP) that applies Natural Language Processing (NLP), machine learning, deep learning, transformer-based sentiment classification, brand reputation analytics, and Large Language Models (LLMs) to analyse online customer reviews and transform them into decision-support information.

The current case study focuses on **Spotify application reviews** collected from multiple publicly available Kaggle datasets.

The final deployed system uses a fine-tuned **DistilBERT** model to classify reviews into **Positive** or **Negative** sentiment. The predictions are subsequently transformed into brand reputation indicators, issue categories, customer voice insights, department-level AI reports, and an executive management report.

The application is implemented using **Streamlit** and deployed through **Streamlit Community Cloud**.

---

# 📌 Project Overview

Online customer reviews contain valuable information about customer satisfaction, product quality, technical problems, subscription concerns, customer service issues, and overall brand perception.

However, manually analysing thousands of online reviews is difficult and time-consuming.

BrandPulse AI addresses this problem by creating an end-to-end review intelligence system:

```text
Customer Reviews
        │
        ▼
Sentiment Prediction
        │
        ▼
Brand Reputation Analytics
        │
        ▼
Customer Issue Analysis
        │
        ▼
Customer Voice Intelligence
        │
        ▼
AI Department Managers
        │
        ▼
Executive Management Report
        │
        ▼
DOCX / PDF Report Export
```

The system therefore extends conventional sentiment classification beyond simply predicting:

```text
Positive
or
Negative
```

and converts model outputs into information that can support organisational decision-making.

---

# 🎯 Project Objectives

The main objectives of the project are to:

- collect and integrate Spotify application reviews from multiple datasets;
- preprocess online review text for NLP modelling;
- compare different feature representations and sentiment classification models;
- develop and evaluate traditional machine learning, deep learning, hybrid, and transformer approaches;
- deploy the selected DistilBERT sentiment classifier;
- classify Spotify reviews into Positive and Negative sentiment;
- calculate brand-level reputation indicators from sentiment predictions;
- identify recurring customer issues from negative reviews;
- extract frequently occurring positive and negative customer terms;
- provide department-specific interpretations using LLMs;
- generate management recommendations based on analytical evidence;
- consolidate departmental findings into an executive report;
- provide an interactive Streamlit decision-support dashboard;
- support professional report export.

---

# 🏗️ System Architecture

The final BrandPulse AI architecture is:

```text
                     Spotify Reviews
                           │
                           ▼
                  Streamlit Application
                           │
                           ▼
                    DistilBERT Model
                 Hosted on Hugging Face
                           │
                           ▼
              Positive / Negative Sentiment
                           │
                           ▼
                Brand Reputation Analytics
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 Reputation Score     Issue Analysis   Customer Voice
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                 AI Management Council
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
 Gemini Managers    OpenRouter Managers   Department Reports
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                    Executive Manager
                           │
                           ▼
             Executive Reputation Report
                           │
                           ▼
                   DOCX / PDF Export
```

---

# 🧠 Predictive Sentiment Model

## DistilBERT

The final deployed sentiment classifier is a fine-tuned **DistilBERT sequence classification model**.

The model performs binary sentiment classification:

```text
0 → Negative
1 → Positive
```

The deployed model and tokenizer are stored in a Hugging Face repository and loaded by the Streamlit application when required.

The application can analyse:

- one individual review; or
- multiple reviews uploaded through CSV/XLSX files.

---

# 🔍 Example Prediction

Example input:

```text
The latest Spotify update keeps crashing and playback stops randomly.
```

Possible output:

```text
Sentiment:
Negative

Confidence:
96.42%
```

> Model confidence represents the probability produced by the model. It should not be interpreted as a guarantee that the prediction is correct.

---

# 📊 Brand Reputation Analytics

After DistilBERT classifies the reviews, BrandPulse AI aggregates the predictions into brand-level information.

The Reputation Dashboard provides:

- total reviews analysed;
- positive review count;
- negative review count;
- positive review percentage;
- negative review percentage;
- Brand Reputation Score;
- sentiment distribution;
- negative review issue distribution;
- frequent positive terms;
- frequent negative terms;
- representative negative reviews.

---

# 📈 Brand Reputation Score

BrandPulse AI uses the following project-defined indicator:

```text
Brand Reputation Score
=
Positive Reviews
-------------------------------- × 100
Positive Reviews + Negative Reviews
```

For example:

```text
Positive Reviews = 720
Negative Reviews = 280

Brand Reputation Score
= 720 / (720 + 280) × 100
= 72%
```

The prototype interprets the score using the following ranges:

| Brand Reputation Score | Interpretation |
|---:|---|
| 80–100% | Very Positive |
| 60–79.99% | Positive |
| 40–59.99% | Mixed |
| 20–39.99% | Negative |
| 0–19.99% | Very Negative |

> The Brand Reputation Score is a **project-defined decision-support indicator** and is not presented as a universal or industry-standard brand reputation index.

---

# 🔎 Customer Issue Analysis

Negative customer reviews are further analysed using predefined issue categories.

Current categories include:

- Technical Performance
- Playback
- Subscription and Pricing
- Advertisements
- Account and Login
- Playlist and Library
- User Interface
- Customer Service
- Other or Unclear

A review can belong to more than one issue category.

For example:

```text
Review:
"The app keeps crashing and playback stops every few minutes."

Detected Issues:
- Technical Performance
- Playback
```

Issue counts should therefore be interpreted as **issue mentions**, rather than necessarily representing unique reviews.

---

# 💬 Customer Voice Intelligence

BrandPulse AI extracts frequently occurring terms from predicted:

```text
Positive reviews
```

and:

```text
Negative reviews
```

This provides an additional view of recurring customer language.

Example:

```text
Positive Customer Voice

music        42
playlist     31
love         27
great        24
recommend    18
```

The objective is to help users identify words and topics commonly associated with positive or negative customer experiences.

---

# 🧩 Separation of System Components

An important design principle of BrandPulse AI is that sentiment prediction, issue analysis, and management recommendation generation are separate components.

```text
DistilBERT
│
└── Sentiment Prediction


Python Analytics Layer
│
├── Brand Reputation Score
├── Sentiment Distribution
├── Issue Categorisation
└── Customer Voice Analysis


Large Language Models
│
├── Departmental Interpretation
├── Management Recommendations
└── Executive Consolidation
```

The LLMs therefore **do not replace the trained DistilBERT model**.

They receive structured analytical evidence produced after sentiment prediction.

---

# 🤖 AI Management Council

The application contains five role-based AI department managers.

Each manager receives the same structured brand reputation evidence but analyses it according to a different organisational responsibility.

Current manager-provider assignment:

| AI Manager | LLM Provider |
|---|---|
| Technical Manager | Gemini |
| Product Manager | Gemini |
| Customer Service Manager | Gemini |
| Marketing Manager | OpenRouter Free |
| Subscription Manager | OpenRouter Free |
| Executive Manager | Gemini |

This assignment is used as part of the prototype architecture and should not be interpreted as a claim that one provider is universally better for a particular department.

---

# 🛠️ Technical Manager

**Provider:** Gemini

The Technical Manager focuses on:

- software stability;
- application crashes;
- technical failures;
- playback problems;
- application performance;
- reliability;
- recurring technical complaints.

Example management considerations may include:

- prioritising high-frequency technical issues;
- reducing crash rates;
- monitoring software reliability;
- improving playback stability;
- establishing technical performance KPIs.

---

# 🧩 Product Manager

**Provider:** Gemini

The Product Manager focuses on:

- application features;
- usability;
- playlists;
- navigation;
- product experience;
- feature requests;
- product improvement opportunities.

The Product Manager interprets review evidence from a product development perspective.

---

# 🎧 Customer Service Manager

**Provider:** Gemini

The Customer Service Manager focuses on:

- complaints;
- customer satisfaction;
- customer frustration;
- recurring support problems;
- service recovery;
- customer communication;
- complaint response priorities.

---

# 📣 Marketing Manager

**Provider:** OpenRouter Free

The Marketing Manager focuses on:

- brand perception;
- positive customer experiences;
- reputation weaknesses;
- communication strategies;
- reputation risks;
- customer-facing messaging;
- brand positioning.

The application currently requests:

```text
openrouter/free
```

OpenRouter may select different free models depending on availability.

Therefore, the actual underlying OpenRouter model used to generate a report is recorded and displayed by the application.

---

# 💳 Subscription Manager

**Provider:** OpenRouter Free

The Subscription Manager focuses on:

- Premium subscription experiences;
- subscription pricing;
- billing concerns;
- advertisements;
- perceived customer value;
- subscription satisfaction;
- potential retention issues.

The application also records the actual free model selected by OpenRouter for transparency.

---

# 👔 Executive Manager

The Executive Manager uses **Gemini**.

It becomes available only after all five department manager reports have been generated.

The Executive Manager consolidates department-level findings into an organisation-wide report.

The final Executive Report may contain sections such as:

- Executive Summary
- Overall Brand Reputation
- Main Brand Strengths
- Critical Brand Risks
- Major Customer Issues
- Department-Level Findings
- Immediate Priorities
- Short-Term Improvement Actions
- Long-Term Improvement Actions
- Recommended KPIs
- Management Recommendations
- Limitations

---

# 📑 Professional Report Export

BrandPulse AI is designed to support professional export of the generated analysis.

Supported report formats include:

## Microsoft Word

```text
BrandPulse_AI_Brand_Reputation_Report.docx
```

## PDF

```text
BrandPulse_AI_Brand_Reputation_Report.pdf
```

The complete report may contain:

1. Brand Reputation Overview
2. Sentiment Results
3. Brand Reputation Score
4. Issue Analysis
5. Customer Voice Intelligence
6. Representative Negative Reviews
7. Technical Manager Report
8. Product Manager Report
9. Customer Service Manager Report
10. Marketing Manager Report
11. Subscription Manager Report
12. Executive Brand Reputation Report
13. System Interpretation Notes
14. Limitations

> DOCX and PDF generation remain part of the final system testing process.

---

# 🖥️ Streamlit Application

The final interface contains four main sections.

---

## 🧪 Single Review

Allows one customer review to be entered manually.

Workflow:

```text
Customer Review
      │
      ▼
DistilBERT
      │
      ▼
Positive / Negative
      │
      ▼
Prediction Confidence
```

---

## 📂 Batch Intelligence

Allows users to upload multiple reviews using:

```text
.csv
.xlsx
```

A dataset only needs a column containing customer review text.

Example:

```csv
review_text
"Spotify has excellent music recommendations."
"The application keeps crashing after the update."
"Premium has become too expensive."
```

After uploading the file, the user selects the column containing the review text.

The system then performs batch sentiment classification.

---

## 📈 Reputation Dashboard

The Reputation Dashboard visualises the results using:

- KPI cards;
- sentiment distribution charts;
- Brand Reputation Score;
- negative issue distributions;
- positive customer voice;
- negative customer voice;
- representative negative customer reviews.

---

## 🤖 AI Management Council

This section contains:

```text
Technical Manager
Product Manager
Customer Service Manager
Marketing Manager
Subscription Manager
Executive Manager
```

The manager reports depend on the results generated through Batch Intelligence.

---

# 📂 Repository Structure

The current project repository follows approximately this structure:

```text
FYP-Brand-Reputation-System/
│
├── .streamlit/
│   └── config.toml
│
├── notebooks/
│   ├── README.md
│   ├── FYP_Single_Algorithm.ipynb
│   ├── FYP_DistilBERT.ipynb
│   └── FYP_Hybrid.ipynb
│
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── distilbert_predictor.py
│   ├── llm_service.py
│   └── report_export.py
│
├── streamlit_app.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# 📓 Experimental Notebooks

The `notebooks/` folder contains the experimental model-development workflow.

Additional information is available in:

```text
notebooks/README.md
```

---

# 1️⃣ FYP_Single_Algorithm.ipynb

This notebook contains the main experimental pipeline for:

- dataset preparation;
- exploratory analysis;
- complete text preprocessing;
- feature representation;
- individual machine-learning experiments;
- deep-learning experiments;
- model comparison.

## Important Preprocessing Note

The **complete text preprocessing workflow is implemented only in this notebook**.

The processed datasets are saved as:

```text
.csv
.xlsx
```

files for reuse by the DistilBERT and Hybrid notebooks.

Conceptually:

```text
Raw Datasets
      │
      ▼
FYP_Single_Algorithm.ipynb
      │
      ├── Dataset Integration
      ├── Full Text Preprocessing
      ├── Feature Representation
      └── Model Experiments
      │
      ▼
Saved Preprocessed CSV / XLSX
```

---

# 2️⃣ FYP_DistilBERT.ipynb

This notebook contains the DistilBERT transformer experiment.

It includes:

- loading the saved preprocessed dataset;
- train/validation/test preparation;
- tokenisation;
- class-weight preparation;
- DistilBERT fine-tuning;
- validation;
- final evaluation;
- confusion matrix generation;
- model export;
- tokenizer export;
- Hugging Face deployment preparation.

The complete preprocessing pipeline is **not repeated** in this notebook.

Instead:

```text
FYP_Single_Algorithm.ipynb
        │
        ▼
Saved Preprocessed Dataset
        │
        ▼
FYP_DistilBERT.ipynb
```

The current Streamlit deployment uses the DistilBERT model produced from this workflow.

---

# 3️⃣ FYP_Hybrid.ipynb

This notebook contains the hybrid modelling experiments.

The Hybrid notebook may involve:

- loading saved preprocessed datasets;
- loading selected feature representations;
- using high-performing modelling components;
- generating predictions;
- combining prediction outputs;
- applying hybrid/fusion techniques;
- comparing hybrid performance against individual models.

The full preprocessing pipeline is also **not repeated** in the Hybrid notebook.

Instead:

```text
FYP_Single_Algorithm.ipynb
        │
        ▼
Saved CSV / XLSX Datasets
        │
        ▼
FYP_Hybrid.ipynb
```

The Hybrid notebook is retained for experimental comparison and is not the final model deployed by Streamlit.

---

# 🔁 Recommended Notebook Execution Order

To reproduce the complete modelling workflow:

```text
STEP 1
FYP_Single_Algorithm.ipynb
        │
        ├── Load raw datasets
        ├── Integrate datasets
        ├── Full preprocessing
        ├── Individual experiments
        └── Save processed CSV / XLSX
        │
        ▼

STEP 2
FYP_DistilBERT.ipynb
        │
        ├── Load saved dataset
        ├── Fine-tune DistilBERT
        ├── Validate / Test
        └── Export final model
        │
        ▼

STEP 3
FYP_Hybrid.ipynb
        │
        ├── Load saved dataset(s)
        ├── Run hybrid experiments
        └── Compare performance
```

The DistilBERT and Hybrid notebooks should therefore not be expected to independently recreate the complete text preprocessing stage.

---

# 📊 Dataset Sources

The project uses four Spotify-related review datasets obtained from Kaggle.

---

## Dataset 1 — Top 20 Play Store App Reviews Daily Update

Spotify file:

```text
Spotify.csv
```

Source:

https://www.kaggle.com/datasets/odins0n/top-20-play-store-app-reviews-daily-update?select=Spotify.csv

---

## Dataset 2 — App Store Music App Reviews

Source:

https://www.kaggle.com/datasets/cluesec/app-store-music-app-reviews

---

## Dataset 3 — Top 10 Global Apps Play Store Reviews

Source:

https://www.kaggle.com/datasets/nitinchoudhary012/top-10-global-apps-play-store-reviews

---

## Dataset 4 — Spotify App Reviews 2022

Source:

https://www.kaggle.com/datasets/mfaaris/spotify-app-reviews-2022

---

# 📚 Dataset Attribution

The datasets were obtained from Kaggle for academic research purposes.

Users reproducing the project should refer to the respective Kaggle pages for:

- original dataset authorship;
- licensing information;
- usage terms;
- latest dataset versions.

The datasets are not redistributed as part of this repository unless permitted by the applicable dataset licence.

---

# ☁️ Google Colab

The experimental notebooks were primarily developed in **Google Colab**.

Google Drive is commonly mounted using:

```python
from google.colab import drive

drive.mount(
    "/content/drive"
)
```

Files are then accessed through paths such as:

```text
/content/drive/MyDrive/...
```

---

# ⚠️ Important Google Drive Path Requirement

Some notebook code uses paths based on the original Google Drive structure used during development.

For example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "spotify_preprocessed_output/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

These paths may not exist when another user runs the notebook.

Users must change the paths according to their own Google Drive structure.

For example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "FYP/Datasets/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

This applies to:

- original/raw datasets;
- preprocessed datasets;
- TF-IDF datasets;
- embedding datasets;
- CSV files;
- XLSX files;
- model checkpoints;
- saved model folders;
- validation results;
- prediction exports;
- Hugging Face export directories.

---

# ❌ FileNotFoundError

A common error when reproducing the notebooks is:

```text
FileNotFoundError:
[Errno 2] No such file or directory
```

This normally means the configured path does not match the current Google Drive directory.

Users can inspect their Google Drive using:

```python
import os

print(
    os.listdir(
        "/content/drive/MyDrive"
    )
)
```

and modify the file path accordingly.

---

# 💾 Preprocessed CSV / XLSX Dependency

A particularly important project detail is:

```text
FULL TEXT PREPROCESSING
        │
        ▼
FYP_Single_Algorithm.ipynb
```

The other experimental notebooks mainly consume saved preprocessing outputs.

Therefore:

```text
FYP_DistilBERT.ipynb
→ loads saved processed data

FYP_Hybrid.ipynb
→ loads saved processed data
```

If the required files have not yet been generated, the relevant preprocessing/export sections of `FYP_Single_Algorithm.ipynb` must be completed first.

---

# 🔬 Experimental Approaches

The project investigates several NLP modelling approaches.

---

## TF-IDF Representations

Experiments may include:

```text
Unigram

Unigram + Bigram

Unigram + Bigram + Trigram
```

---

## Embedding Representations

Experiments may include:

```text
Word2Vec

GloVe

FastText
```

---

## Traditional Machine Learning

Models investigated may include:

- Naive Bayes
- Support Vector Machine
- Logistic Regression

Different Naive Bayes variants can be used depending on the feature representation, such as:

```text
TF-IDF
→ MultinomialNB

Embedding Features
→ GaussianNB
```

---

## Deep Learning

Experiments may include:

- LSTM
- BiLSTM
- CNN

---

## Transformer

The transformer experiment uses:

```text
DistilBERT
```

The selected DistilBERT model is the model currently used by the deployed BrandPulse AI application.

---

## Hybrid Experiment

A separate notebook investigates hybrid/fusion approaches based on selected experimental results.

The Hybrid model is retained as experimental evidence and is not currently used as the final Streamlit sentiment predictor.

---

# 📏 Evaluation Metrics

The modelling notebooks evaluate classification performance using metrics such as:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Model selection is based on the experimental methodology implemented in the notebooks.

The final test set should remain separate from the training and model-selection stages.

---

# 🌐 Hugging Face Model Deployment

After the final DistilBERT model is trained, the model and tokenizer are exported.

Typical files include:

```text
config.json
model.safetensors
tokenizer_config.json
special_tokens_map.json
vocab.txt
```

The exported model is uploaded to Hugging Face.

The Streamlit application loads the model using:

```text
Hugging Face Repository
        │
        ▼
AutoTokenizer
        │
        ▼
AutoModelForSequenceClassification
        │
        ▼
BrandPulse AI
```

The Hugging Face repository can remain private when a valid read token is supplied through Streamlit Secrets.

---

# 🛠️ Technology Stack

## Programming Language

- Python

## Data Processing

- pandas
- NumPy
- openpyxl

## Machine Learning / NLP

- scikit-learn
- PyTorch
- Hugging Face Transformers
- DistilBERT

## Embedding / Feature Representation

- TF-IDF
- Word2Vec
- GloVe
- FastText

## Deep Learning

- LSTM
- BiLSTM
- CNN

## Model Hosting

- Hugging Face Hub

## Generative AI

- Google Gemini
- OpenRouter

## Visualisation

- Streamlit
- Plotly

## Reporting

- python-docx
- fpdf2

## Development

- Google Colab
- GitHub

## Cloud Deployment

- Streamlit Community Cloud

---

# 📦 Main Application Dependencies

The deployed application currently uses packages such as:

```text
streamlit
torch
transformers
huggingface_hub
safetensors
pandas
numpy
openpyxl
plotly
requests
google-genai>=2.3.0
python-docx
fpdf2
```

Dependencies are listed in:

```text
requirements.txt
```

---

# 🔐 Environment Secrets

Sensitive API credentials should not be stored directly in GitHub source files.

The Streamlit deployment requires secrets similar to:

```toml
HF_MODEL_REPO = "YOUR_HUGGINGFACE_MODEL_REPOSITORY"

HF_TOKEN = "YOUR_HUGGINGFACE_READ_TOKEN"

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

GEMINI_MODEL = "YOUR_CONFIGURED_GEMINI_MODEL"

OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

OPENROUTER_MODEL = "openrouter/free"
```

Actual credentials must be configured through Streamlit Secrets or another secure environment-variable system.

> Never commit real Hugging Face, Gemini, OpenRouter, or other private API keys to GitHub.

If an API key has accidentally been committed, revoke the exposed credential and generate a replacement.

---

# 🚀 Running BrandPulse AI Locally

## 1. Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd FYP-Brand-Reputation-System
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure required secrets

Set the required Hugging Face, Gemini, and OpenRouter credentials.

---

## 4. Start Streamlit

```bash
streamlit run streamlit_app.py
```

Streamlit will display a local URL in the terminal.

---

# ☁️ Streamlit Community Cloud Deployment

The deployment configuration uses approximately:

```text
Repository:
FYP-Brand-Reputation-System

Branch:
main

Main file:
streamlit_app.py
```

The required secrets must be configured in Streamlit Community Cloud before the application can access:

- Hugging Face;
- Gemini;
- OpenRouter.

---

# 🧪 Current Testing Status

BrandPulse AI has been progressively tested during development using smaller review samples and individual component tests.

Components tested during development include:

```text
✅ Hugging Face DistilBERT model loading

✅ Single-review DistilBERT prediction

✅ CSV/XLSX upload interface

✅ Batch prediction workflow on manageable samples

✅ Brand Reputation Dashboard

✅ Brand Reputation Score calculation

✅ Customer issue analysis

✅ Customer voice analysis

✅ Gemini API connectivity

✅ OpenRouter API connectivity

✅ Department manager generation workflow

✅ Executive Manager workflow

🧪 DOCX / PDF final export verification

🧪 Full-scale Streamlit dataset testing
```

The complete full-scale FYP dataset has **not necessarily been processed end-to-end through Streamlit Community Cloud**.

Large-scale inference through a free cloud deployment can be affected by:

- memory limits;
- CPU availability;
- model inference time;
- Streamlit execution limits;
- application restarts;
- third-party API quotas.

Therefore:

```text
Google Colab / Experimental Notebooks
→ Model development
→ Training
→ Validation
→ Testing
→ Experimental comparison

Streamlit
→ Deployment prototype
→ Interactive prediction
→ Reputation visualisation
→ Decision-support demonstration
```

A manageable representative review sample is recommended for the live Streamlit demonstration.

---

# ⚠️ Known Limitations

## 1. Streamlit Community Cloud Resources

The final DistilBERT model requires computational resources for inference.

Processing a very large review dataset directly through Streamlit Community Cloud may result in:

- slow processing;
- timeout;
- high memory consumption;
- application restart.

Therefore, the deployed system is primarily intended as a decision-support prototype rather than a high-volume production inference service.

---

## 2. Gemini API Rate Limits

Gemini API access is subject to usage quotas.

For example:

```text
429 RESOURCE_EXHAUSTED
```

may occur if the current project exceeds an assigned request or token limit.

This does not necessarily indicate an error in the BrandPulse AI application.

---

## 3. OpenRouter Free Router

BrandPulse AI currently requests:

```text
openrouter/free
```

The actual LLM selected by OpenRouter may vary according to free-model availability.

Therefore, Marketing and Subscription reports may not always use the same underlying model.

The application records the actual selected OpenRouter model where available.

---

## 4. DistilBERT Classification Errors

The final sentiment classifier is a predictive model.

Incorrect sentiment predictions can still occur.

Model confidence should therefore not be interpreted as certainty.

---

## 5. Binary Sentiment

The deployed system currently focuses on:

```text
Positive
Negative
```

The neutral category is not part of the final deployed binary classification workflow.

---

## 6. Rule-Based Issue Categorisation

Issue categorisation uses predefined keyword/rule logic.

As a result:

- one review may match multiple issues;
- an issue may not be detected if different wording is used;
- some reviews may be categorised as Other or Unclear.

A trained multi-label issue classifier could improve this component in future work.

---

## 7. LLM Hallucination

Gemini and OpenRouter models can potentially generate unsupported or inaccurate statements.

Prompts are designed to encourage the models to:

- use supplied analytical evidence;
- avoid inventing statistics;
- distinguish observations from recommendations;
- state limitations when evidence is insufficient.

However, generated reports should still be treated as **decision-support outputs** rather than independently verified factual conclusions.

---

# 🧪 Recommended System Testing

A complete functional test should include:

| Test | Expected Result |
|---|---|
| Positive single review | Positive prediction |
| Negative single review | Negative prediction |
| Empty review | Warning displayed |
| CSV upload | File accepted |
| XLSX upload | File accepted |
| Missing review values | Safely removed/ignored |
| Batch sentiment prediction | Predictions generated |
| Reputation Dashboard | Statistics displayed |
| Sentiment chart | Positive/negative distribution displayed |
| Issue analysis | Issue mentions displayed |
| Customer voice | Frequent terms displayed |
| Gemini Technical Manager | Report generated |
| Gemini Product Manager | Report generated |
| Gemini Customer Service Manager | Report generated |
| OpenRouter Marketing Manager | Report generated |
| OpenRouter Subscription Manager | Report generated |
| Executive Manager before 5 reports | Generation prevented |
| Executive Manager after 5 reports | Report generated |
| DOCX export | Word file opens correctly |
| PDF export | PDF opens correctly |
| New dataset uploaded | Previous manager reports cleared |

---

# 🧪 Recommended Live Demonstration Workflow

For the FYP presentation or system demonstration:

```text
1. Open BrandPulse AI
        │
        ▼
2. Enter one positive review
        │
        ▼
3. Run Single Review prediction
        │
        ▼
4. Enter one negative review
        │
        ▼
5. Upload representative CSV
        │
        ▼
6. Run Batch Intelligence
        │
        ▼
7. Open Reputation Dashboard
        │
        ▼
8. Explain Brand Reputation Score
        │
        ▼
9. Explain Issue Analysis
        │
        ▼
10. Generate Department Manager Reports
        │
        ▼
11. Generate Executive Report
        │
        ▼
12. Export DOCX / PDF Report
```

A smaller representative dataset is recommended during a live demonstration to reduce the risk of cloud resource limitations.

---

# 🧪 Large Dataset Testing

The original FYP modelling workflow uses a substantially larger review dataset than the small demonstration dataset required by Streamlit.

The full-scale data is more appropriately processed in:

```text
Google Colab
```

because it provides a controlled model-development environment with access to higher computational resources.

Streamlit serves primarily as the:

- deployment interface;
- visualisation layer;
- management decision-support system;
- demonstration platform.

---

# 🧰 Troubleshooting

## FileNotFoundError in notebooks

Cause:

```text
Google Drive path does not match the current user's Drive.
```

Solution:

Update:

```text
/content/drive/MyDrive/...
```

to match the actual location of the dataset.

---

## Hugging Face Model Error

Check:

- `HF_MODEL_REPO`;
- `HF_TOKEN`;
- repository permissions;
- model files;
- tokenizer files.

---

## Gemini 429 Error

Example:

```text
429 RESOURCE_EXHAUSTED
```

This usually indicates an API quota or rate limit.

Wait before retrying and check the configured API quota.

Repeatedly clicking the generation button should be avoided while a rate limit is active.

---

## OpenRouter Error

Check:

- API key;
- free-model availability;
- API request limits;
- response model information.

Because `openrouter/free` is used, free model availability may change.

---

# 🔐 Security Recommendations

Before submitting or demonstrating the FYP:

- ensure no API keys exist in source code;
- ensure no Hugging Face write token exists in GitHub;
- ensure Gemini API keys are only stored securely;
- ensure OpenRouter keys are only stored securely;
- inspect notebooks for accidentally printed credentials;
- revoke any credential that has previously been publicly exposed.

---

# 📌 Academic Transparency

The repository separates experimental research from the final deployment.

```text
notebooks/
→ Research experiments
→ Model development
→ Model evaluation
→ Comparison


src/
→ Application modules
→ Prediction
→ Analytics
→ LLM integration
→ Report generation


streamlit_app.py
→ Interactive decision-support system
```

The experimental notebooks provide evidence of model development, while the Streamlit application demonstrates how the selected model can be integrated into a practical brand reputation decision-support prototype.

---

# 🔮 Future Improvements

Potential future improvements include:

- higher-capacity cloud inference;
- asynchronous/background batch processing;
- queue-based review processing;
- database integration;
- direct Google Play/App Store data collection;
- historical brand reputation tracking;
- reputation trend visualisation;
- multilingual review analysis;
- topic modelling;
- transformer-based issue classification;
- multi-label customer issue classification;
- retrieval-augmented generation;
- automated LLM grounding checks;
- LLM output evaluation;
- management KPI tracking;
- scheduled reputation monitoring;
- user authentication;
- department-specific dashboards;
- improved DOCX/PDF visual report design;
- support for additional brands;
- comparative competitor reputation analysis.

---

# 📊 Final System Component Summary

| Component | Technology | Purpose |
|---|---|---|
| Review Input | Streamlit | Receive customer reviews |
| Sentiment Prediction | DistilBERT | Positive/Negative classification |
| Model Hosting | Hugging Face | Store deployed transformer |
| Reputation Score | Python | Aggregate sentiment into reputation indicator |
| Issue Analysis | Python rules | Detect common customer concerns |
| Customer Voice | Python | Extract frequent terms |
| Technical Manager | Gemini | Technical recommendations |
| Product Manager | Gemini | Product recommendations |
| Customer Service Manager | Gemini | Customer service recommendations |
| Marketing Manager | OpenRouter Free | Marketing recommendations |
| Subscription Manager | OpenRouter Free | Pricing/subscription recommendations |
| Executive Manager | Gemini | Consolidate management findings |
| Dashboard | Streamlit + Plotly | Interactive visualisation |
| DOCX Export | python-docx | Editable management report |
| PDF Export | fpdf2 | Fixed-format report |

---

# 📂 Recommended Final Repository Structure

```text
FYP-Brand-Reputation-System/
│
├── .streamlit/
│   └── config.toml
│
├── notebooks/
│   ├── README.md
│   ├── FYP_Single_Algorithm.ipynb
│   ├── FYP_DistilBERT.ipynb
│   └── FYP_Hybrid.ipynb
│
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── distilbert_predictor.py
│   ├── llm_service.py
│   └── report_export.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ✅ Current Project Status

```text
✅ Spotify review dataset preparation

✅ Full text preprocessing workflow

✅ TF-IDF experiments

✅ Embedding experiments

✅ Traditional machine-learning experiments

✅ Deep-learning experiments

✅ DistilBERT experiment

✅ Hybrid experiment

✅ Final DistilBERT model export

✅ Hugging Face model hosting

✅ Streamlit deployment

✅ Single Review prediction

✅ Batch Intelligence workflow

✅ Reputation Dashboard

✅ Brand Reputation Score

✅ Customer Issue Analysis

✅ Customer Voice Analysis

✅ Gemini integration

✅ OpenRouter integration

✅ Five AI Department Managers

✅ Executive Manager workflow

🔄 DOCX / PDF final verification

🔄 Final functional testing

🔄 LLM report evaluation

🔄 Final FYP documentation and presentation
```

---

# ⚖️ Disclaimer

BrandPulse AI is an **academic Final Year Project prototype**.

The application demonstrates how NLP-based sentiment classification, brand reputation analytics, and Large Language Models can be combined within a decision-support workflow.

The model predictions and generated management recommendations should not be interpreted as:

- official Spotify statements;
- independently verified business facts;
- guaranteed predictions;
- professional management advice;
- actual decisions made by Spotify.

Spotify is used solely as the application-review case study.

This project is not affiliated with, sponsored by, or endorsed by Spotify.

---

# 📚 Final Year Project Information

**Project Title:**  
Online Review-Based Brand Reputation Prediction Using NLP Techniques

**System Name:**  
BrandPulse AI

**Application Domain:**  
Spotify Online Customer Reviews

**Primary Deployed Sentiment Model:**  
DistilBERT

**Sentiment Classes:**  
Positive and Negative

**Experimental Environment:**  
Google Colab

**Model Hosting:**  
Hugging Face

**Application Framework:**  
Streamlit

**Cloud Deployment:**  
Streamlit Community Cloud

**Generative AI Providers:**  
Google Gemini and OpenRouter

**Report Formats:**  
DOCX and PDF

---

# 📝 Summary

BrandPulse AI combines three main levels of intelligence:

```text
1. Predictive Intelligence
   │
   └── DistilBERT sentiment classification


2. Analytical Intelligence
   │
   ├── Brand Reputation Score
   ├── Sentiment Distribution
   ├── Issue Analysis
   └── Customer Voice


3. Generative Management Intelligence
   │
   ├── Technical Manager
   ├── Product Manager
   ├── Customer Service Manager
   ├── Marketing Manager
   ├── Subscription Manager
   └── Executive Manager
```

The experimental notebooks provide the modelling foundation, while the final Streamlit system demonstrates how the selected DistilBERT model can be transformed into an interactive **brand reputation decision-support platform**.
