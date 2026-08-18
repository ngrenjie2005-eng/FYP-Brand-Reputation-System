# 🎧 BrandPulse AI

## Online Review-Based Brand Reputation Prediction Using NLP Techniques

**BrandPulse AI** is a Final Year Project (FYP) that applies Natural Language Processing (NLP), machine learning, deep learning, transformer-based sentiment classification, brand reputation analytics, and Large Language Models (LLMs) to analyse online customer reviews and transform them into management-oriented decision-support information.

The project uses **Spotify application reviews** as the case study.

The final system deploys a fine-tuned **DistilBERT** model to classify reviews into **Positive** or **Negative** sentiment. These predictions are subsequently transformed into brand reputation indicators, customer issue categories, customer voice insights, department-level AI management reports, and an executive-level brand reputation report.

The completed application is implemented using **Streamlit** and deployed through **Streamlit Community Cloud**.

---

# 📌 Project Overview

Online customer reviews contain valuable information about:

- customer satisfaction;
- application performance;
- product usability;
- technical problems;
- playback issues;
- subscription concerns;
- advertisements;
- customer service;
- brand perception.

However, manually analysing a large number of customer reviews is time-consuming and difficult.

BrandPulse AI provides an integrated workflow:

```text
Customer Reviews
        │
        ▼
DistilBERT Sentiment Prediction
        │
        ▼
Brand Reputation Analytics
        │
        ├── Reputation Score
        ├── Sentiment Distribution
        ├── Customer Issue Analysis
        └── Customer Voice Analysis
        │
        ▼
Multi-LLM AI Management Council
        │
        ├── Technical Manager
        ├── Product Manager
        ├── Customer Service Manager
        ├── Marketing Manager
        └── Subscription Manager
        │
        ▼
Executive Manager
        │
        ▼
Executive Brand Reputation Report
        │
        ▼
DOCX / PDF Report Export
```

The system therefore extends conventional sentiment analysis beyond simply producing:

```text
Positive
or
Negative
```

and converts the predictive results into information that can support managerial interpretation and decision-making.

---

# 🎯 Project Objectives

The main objectives of BrandPulse AI are to:

- collect and integrate Spotify application reviews from multiple sources;
- preprocess customer review text for NLP modelling;
- compare different feature representations and sentiment classification approaches;
- evaluate traditional machine learning, deep learning, transformer, and hybrid approaches;
- deploy a selected DistilBERT sentiment classification model;
- classify reviews into Positive and Negative sentiment;
- calculate brand-level reputation indicators;
- identify common customer issues within negative reviews;
- analyse recurring positive and negative customer language;
- generate department-specific AI management reports;
- distribute generative AI workloads across multiple LLM providers;
- consolidate department reports into an executive-level report;
- provide interactive visualisation through Streamlit;
- generate professional Microsoft Word and PDF reports.

---

# 🏗️ Final System Architecture

The final BrandPulse AI architecture consists of three main intelligence layers:

```text
                    Spotify Reviews
                          │
                          ▼
                 Streamlit Application
                          │
                          ▼
                  Predictive AI Layer
                          │
                    DistilBERT
                          │
                          ▼
              Positive / Negative Sentiment
                          │
                          ▼
                  Analytics Layer
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
 Reputation Score    Issue Analysis   Customer Voice
         │                │                │
         └────────────────┼────────────────┘
                          │
                          ▼
             Multi-LLM Management Layer
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
 OpenRouter Free     Ollama Cloud      Department Reports
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
                  Executive Manager
                       Gemini
                          │
                          ▼
              Executive Reputation Report
                          │
                          ▼
                  DOCX / PDF Export
```

---

# 🧠 Predictive AI Layer

## DistilBERT

The final deployed sentiment classifier is a fine-tuned **DistilBERT sequence classification model**.

The model performs binary sentiment classification:

```text
0 → Negative
1 → Positive
```

The trained model and tokenizer are hosted in a Hugging Face model repository.

The Streamlit application loads the model and tokenizer directly from Hugging Face during application execution.

---

# 🔍 Single Review Prediction

Users can manually enter one Spotify review.

Example:

```text
The latest Spotify update keeps crashing and playback stops randomly.
```

Possible result:

```text
Sentiment:
Negative

Confidence:
96.42%
```

The application displays:

- predicted sentiment;
- prediction confidence;
- a short interpretation.

> Model confidence represents the probability produced by the classifier and should not be interpreted as certainty.

---

# 📂 Batch Review Intelligence

BrandPulse AI supports batch review analysis through:

```text
.csv
.xlsx
```

The uploaded dataset only requires a column containing customer review text.

Example:

```csv
review_text
"Spotify has excellent music recommendations."
"The latest update keeps crashing."
"Premium is becoming too expensive."
```

Users select the appropriate review-text column before starting the analysis.

The system then performs:

```text
Uploaded Dataset
        ↓
Valid Review Filtering
        ↓
DistilBERT Batch Prediction
        ↓
Sentiment Results
        ↓
Reputation Analytics
```

---

# 📊 Brand Reputation Analytics

After sentiment prediction, BrandPulse AI aggregates individual review predictions into brand-level indicators.

The dashboard provides:

- total reviews analysed;
- positive review count;
- negative review count;
- positive review percentage;
- negative review percentage;
- Brand Reputation Score;
- sentiment distribution;
- negative review issue analysis;
- frequent positive terms;
- frequent negative terms;
- representative negative customer reviews.

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

Example:

```text
Positive Reviews = 720
Negative Reviews = 280

Brand Reputation Score
= 720 / (720 + 280) × 100
= 72%
```

The prototype interprets the resulting value as:

| Score | Interpretation |
|---:|---|
| 80–100% | Very Positive Brand Reputation |
| 60–79.99% | Positive Brand Reputation |
| 40–59.99% | Mixed Brand Reputation |
| 20–39.99% | Negative Brand Reputation |
| 0–19.99% | Very Negative Brand Reputation |

> The Brand Reputation Score is a **project-defined decision-support indicator**. It is not presented as an official Spotify metric or a universal industry-standard brand reputation measurement.

---

# 🔎 Customer Issue Analysis

Negative reviews are analysed using predefined issue categories.

The current categories include:

- Technical Performance
- Playback
- Subscription and Pricing
- Advertisements
- Account and Login
- Playlist and Library
- User Interface
- Customer Service
- Other or Unclear

Example:

```text
Review:
"The app keeps crashing and playback stops every few minutes."

Detected Issues:
- Technical Performance
- Playback
```

A single review may contain multiple issue categories.

Therefore, issue counts are interpreted as:

```text
Issue Mentions
```

rather than necessarily representing unique reviews.

---

# 💬 Customer Voice Intelligence

BrandPulse AI extracts frequently occurring terms from predicted:

```text
Positive Reviews
```

and:

```text
Negative Reviews
```

Example:

```text
Positive Customer Voice

music        42
playlist     31
love         27
great        24
recommend    18
```

This component provides additional insight into recurring customer language and common areas associated with satisfaction or dissatisfaction.

---

# 🧩 Separation of System Components

BrandPulse AI intentionally separates predictive AI, analytical processing, and generative AI.

```text
DistilBERT
│
└── Sentiment Prediction


Python Analytics Layer
│
├── Brand Reputation Score
├── Sentiment Distribution
├── Customer Issue Analysis
└── Customer Voice Analysis


Generative AI Layer
│
├── Department Interpretation
├── Management Recommendations
└── Executive Consolidation
```

The LLMs do **not** replace DistilBERT.

Instead:

```text
DistilBERT
→ predicts sentiment

Python Analytics
→ produces structured evidence

LLMs
→ interpret evidence
→ generate recommendations
```

---

# 🤖 Multi-LLM AI Management Council

The final system uses a **multi-provider Large Language Model architecture**.

This design distributes department-level report generation across different AI providers instead of relying entirely on one LLM service.

The final configuration is:

| Manager | Provider | Model / Route |
|---|---|---|
| Technical Manager | OpenRouter | `openrouter/free` |
| Product Manager | Ollama Cloud | `gpt-oss:20b` |
| Customer Service Manager | OpenRouter | `openrouter/free` |
| Marketing Manager | Ollama Cloud | `gpt-oss:20b` |
| Subscription Manager | OpenRouter | `openrouter/free` |
| Executive Manager | Gemini | Configured through `GEMINI_MODEL` |

The multi-provider architecture helps reduce dependency on a single generative AI provider and mitigates provider-specific quota or availability constraints.

---

# 🌐 OpenRouter Free

OpenRouter is used for:

```text
Technical Manager
Customer Service Manager
Subscription Manager
```

The application requests:

```text
openrouter/free
```

The free router may select different available free models depending on current service availability.

For transparency, BrandPulse AI records and displays:

```text
Provider
Requested Route
Actual Model Used
```

---

# 🦙 Ollama Cloud

Ollama Cloud is used for:

```text
Product Manager
Marketing Manager
```

The current configured model is:

```text
gpt-oss:20b
```

The Ollama managers analyse the same structured reputation evidence as the other department managers but use department-specific role prompts.

---

# ✨ Gemini Executive Manager

Gemini is reserved primarily for the **Executive Manager**.

Instead of using Gemini for several department-level requests, BrandPulse AI preserves Gemini resources for the final consolidation stage.

The Executive Manager receives:

```text
Brand Reputation Analytics
+
Technical Manager Report
+
Product Manager Report
+
Customer Service Manager Report
+
Marketing Manager Report
+
Subscription Manager Report
```

and consolidates them into one organisation-wide report.

The exact Gemini model can be configured through:

```text
GEMINI_MODEL
```

in Streamlit Secrets.

---

# 🛠️ Technical Manager

### Provider

OpenRouter Free

### Focus Areas

The Technical Manager analyses:

- application stability;
- technical performance;
- crashes;
- software bugs;
- playback problems;
- reliability;
- technical customer complaints.

Typical output sections include:

- department overview;
- key findings;
- main reputation risks;
- positive signals;
- recommended actions;
- recommended KPIs;
- priority level;
- limitations.

---

# 🧩 Product Manager

### Provider

Ollama Cloud

### Model

```text
gpt-oss:20b
```

### Focus Areas

The Product Manager analyses:

- product usability;
- application features;
- playlists;
- music library experience;
- navigation;
- user interface;
- product improvement opportunities;
- recurring feature-related complaints.

---

# 🎧 Customer Service Manager

### Provider

OpenRouter Free

### Focus Areas

The Customer Service Manager analyses:

- customer complaints;
- customer dissatisfaction;
- support problems;
- customer communication;
- service recovery;
- recurring customer frustrations.

---

# 📣 Marketing Manager

### Provider

Ollama Cloud

### Model

```text
gpt-oss:20b
```

### Focus Areas

The Marketing Manager analyses:

- brand perception;
- reputation strengths;
- reputation risks;
- positive customer experiences;
- customer communication;
- brand messaging.

---

# 💳 Subscription Manager

### Provider

OpenRouter Free

### Focus Areas

The Subscription Manager analyses:

- Premium subscription;
- pricing;
- advertisements;
- billing;
- perceived value;
- subscription dissatisfaction;
- potential customer retention concerns.

---

# 👔 Executive Manager

### Provider

Gemini

The Executive Manager can only be generated after all five department reports are available.

The Executive Report may contain:

1. Executive Summary
2. Overall Brand Reputation
3. Main Brand Strengths
4. Critical Reputation Risks
5. Cross-Department Findings
6. Immediate Management Priorities
7. Short-Term Action Plan
8. Long-Term Improvement Direction
9. Recommended Executive KPIs
10. Department Coordination
11. Overall Management Recommendation
12. Limitations

---

# 🔄 Management Council Execution Flow

```text
Reputation Analytics Completed
        │
        ▼
Technical Manager
OpenRouter
        │
        ▼
Product Manager
Ollama
        │
        ▼
Customer Service Manager
OpenRouter
        │
        ▼
Marketing Manager
Ollama
        │
        ▼
Subscription Manager
OpenRouter
        │
        ▼
Five Reports Ready
        │
        ▼
Executive Manager
Gemini
        │
        ▼
Executive Report
```

The application stores generated reports using Streamlit session state.

This means changing tabs does not automatically regenerate reports.

---

# 🔄 Report Regeneration Logic

When a department report is regenerated:

```text
Department Report Changed
        ↓
Previous Executive Report
becomes outdated
        ↓
Executive Report cleared
        ↓
New Executive Report required
```

When a new review dataset is analysed:

```text
New Dataset
        ↓
Old Department Reports cleared
        ↓
Old Executive Report cleared
        ↓
Old DOCX/PDF exports cleared
```

This prevents reports from being associated with outdated analytical evidence.

---

# 📑 Professional Report Centre

BrandPulse AI includes a completed professional report-generation component.

The system generates both:

## Microsoft Word

```text
BrandPulse_AI_Brand_Reputation_Report.docx
```

and:

## PDF

```text
BrandPulse_AI_Brand_Reputation_Report.pdf
```

Both formats are generated from the same completed analysis.

---

# 📘 DOCX Report

The Word report is generated using:

```text
python-docx
```

The document contains:

1. Cover Page
2. Brand Reputation Overview
3. Negative Review Issue Analysis
4. Customer Voice Intelligence
5. Representative Negative Reviews
6. Technical Manager Report
7. Product Manager Report
8. Customer Service Manager Report
9. Marketing Manager Report
10. Subscription Manager Report
11. Executive Brand Reputation Report
12. System Interpretation and Limitations

The DOCX version is editable and suitable for further academic formatting if required.

---

# 📕 PDF Report

The PDF report is generated using:

```text
fpdf2
```

The PDF contains the same major analytical and management information as the DOCX report.

The implementation includes:

- page headers;
- page numbers;
- report sections;
- tables;
- customer review examples;
- manager reports;
- executive report;
- interpretation notes;
- system limitations.

---

# 🖥️ Streamlit Application

The final interface contains four primary sections.

---

## 🧪 Single Review

Allows users to manually enter one Spotify review.

```text
Customer Review
        ↓
DistilBERT
        ↓
Positive / Negative
        ↓
Prediction Confidence
```

---

## 📂 Batch Intelligence

Allows users to upload:

```text
CSV
XLSX
```

The system then:

```text
Loads Dataset
        ↓
Select Review Column
        ↓
Removes Missing / Empty Reviews
        ↓
Runs DistilBERT
        ↓
Generates Analytics
```

---

## 📈 Reputation Dashboard

Displays:

- reviews analysed;
- positive reviews;
- negative reviews;
- sentiment percentages;
- Brand Reputation Score;
- sentiment distribution;
- issue distribution;
- positive customer voice;
- negative customer voice;
- representative negative reviews.

---

## 🤖 AI Management Council

Contains:

```text
Technical Manager
Product Manager
Customer Service Manager
Marketing Manager
Subscription Manager
Executive Manager
```

and displays:

- AI provider;
- model used;
- department role;
- generated report;
- download option;
- council completion progress.

---

# 📂 Repository Structure

The final project structure is approximately:

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

# 📓 Experimental Notebooks

The `notebooks/` directory contains three primary experiment notebooks.

---

# 1️⃣ FYP_Single_Algorithm.ipynb

This notebook contains:

- raw dataset loading;
- dataset integration;
- exploratory analysis;
- full text preprocessing;
- feature representation;
- traditional machine-learning experiments;
- deep-learning experiments;
- model comparisons.

## Important

The **complete text preprocessing workflow is implemented only in this notebook**.

Processed datasets are saved into:

```text
CSV
XLSX
```

formats for reuse by the DistilBERT and Hybrid notebooks.

---

# 2️⃣ FYP_DistilBERT.ipynb

This notebook contains:

- loading the previously saved processed dataset;
- train/validation/test preparation;
- tokenisation;
- class-weight configuration;
- DistilBERT fine-tuning;
- model validation;
- model testing;
- evaluation metrics;
- confusion matrix;
- model export;
- tokenizer export;
- Hugging Face deployment preparation.

The complete preprocessing pipeline is **not repeated** here.

Conceptually:

```text
FYP_Single_Algorithm.ipynb
        ↓
Saved Preprocessed Data
        ↓
FYP_DistilBERT.ipynb
```

---

# 3️⃣ FYP_Hybrid.ipynb

The Hybrid notebook contains experiments involving hybrid/fusion approaches.

It may include:

- loading saved processed datasets;
- selected feature representations;
- selected high-performing models;
- prediction generation;
- prediction fusion;
- hybrid representation experiments;
- hybrid performance evaluation;
- comparison against individual models.

The complete preprocessing workflow is also **not repeated** in this notebook.

---

# 🔁 Recommended Notebook Execution Order

```text
STEP 1
FYP_Single_Algorithm.ipynb
        │
        ├── Load raw datasets
        ├── Integrate datasets
        ├── Full text preprocessing
        ├── Individual experiments
        └── Save CSV / XLSX
        │
        ▼

STEP 2
FYP_DistilBERT.ipynb
        │
        ├── Load processed dataset
        ├── Train DistilBERT
        ├── Validate
        ├── Test
        └── Export model
        │
        ▼

STEP 3
FYP_Hybrid.ipynb
        │
        ├── Load processed datasets
        ├── Run hybrid experiments
        └── Compare results
```

---

# 📊 Dataset Sources

Four Spotify-related datasets were obtained from Kaggle.

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

Users reproducing the project should refer to the original Kaggle dataset pages for:

- dataset authorship;
- licences;
- usage conditions;
- latest dataset versions.

---

# ☁️ Google Colab

The experimental notebooks were primarily developed using **Google Colab**.

Google Drive is mounted using code such as:

```python
from google.colab import drive

drive.mount(
    "/content/drive"
)
```

---

# ⚠️ Google Drive Path Requirement

Some notebook code contains file paths based on the original development environment.

For example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "spotify_preprocessed_output/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

These paths must be modified if the notebooks are executed using another Google Drive account.

Example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "FYP/Datasets/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

The same applies to:

- raw dataset locations;
- processed datasets;
- TF-IDF files;
- embedding datasets;
- CSV outputs;
- XLSX outputs;
- checkpoints;
- saved models;
- prediction results;
- deployment folders.

---

# ❌ FileNotFoundError

A common error is:

```text
FileNotFoundError:
[Errno 2] No such file or directory
```

This usually means that the configured path does not match the user's actual Google Drive.

Users can inspect their Google Drive using:

```python
import os

print(
    os.listdir(
        "/content/drive/MyDrive"
    )
)
```

and update the relevant paths accordingly.

---

# 💾 Preprocessed Dataset Dependency

The relationship between notebooks is:

```text
Raw Spotify Reviews
        ↓
FYP_Single_Algorithm.ipynb
        ↓
FULL TEXT PREPROCESSING
        ↓
Saved CSV / XLSX
        │
        ├───────────────┐
        │               │
        ▼               ▼
FYP_DistilBERT     FYP_Hybrid
```

Therefore:

```text
DistilBERT Notebook
→ loads saved processed data

Hybrid Notebook
→ loads saved processed data
```

---

# 🔬 Experimental Approaches

The project investigates several modelling approaches.

## TF-IDF

Representations include:

```text
Unigram

Unigram + Bigram

Unigram + Bigram + Trigram
```

---

# 🧠 Embedding Representations

Experiments include:

```text
Word2Vec

GloVe

FastText
```

---

# 📐 Traditional Machine Learning

Models investigated include approaches such as:

- Naive Bayes
- Support Vector Machine
- Logistic Regression

Different Naive Bayes implementations may be used depending on the feature representation.

For example:

```text
TF-IDF
→ MultinomialNB

Embedding
→ GaussianNB
```

---

# 🧬 Deep Learning

The experimental workflow includes deep-learning models such as:

- LSTM
- BiLSTM
- CNN

---

# 🤖 Transformer Model

The transformer-based experiment uses:

```text
DistilBERT
```

The final Streamlit application deploys the selected DistilBERT model.

---

# 🔗 Hybrid Experiment

The Hybrid notebook investigates combining selected model outputs or feature representations.

The Hybrid approach is retained as experimental evidence and comparative analysis.

It is **not** the final deployed Streamlit sentiment classifier.

---

# 📏 Evaluation Metrics

Model evaluation uses metrics such as:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Validation results are used during model-selection activities.

Final evaluation should be performed using the held-out test set.

---

# 🌐 Hugging Face Deployment

The final DistilBERT model and tokenizer are exported after training.

Typical files include:

```text
config.json
model.safetensors
tokenizer_config.json
special_tokens_map.json
vocab.txt
```

They are uploaded to a Hugging Face model repository.

The Streamlit application then performs:

```text
Hugging Face Repository
        ↓
AutoTokenizer
        ↓
AutoModelForSequenceClassification
        ↓
DistilBERT Prediction
```

---

# 🛠️ Technology Stack

## Programming

- Python

## Development Environment

- Google Colab
- GitHub

## Data Processing

- pandas
- NumPy
- openpyxl

## Machine Learning

- scikit-learn
- PyTorch

## NLP / Transformer

- Hugging Face Transformers
- DistilBERT

## Feature Representation

- TF-IDF
- Word2Vec
- GloVe
- FastText

## Deep Learning

- LSTM
- BiLSTM
- CNN

## Generative AI

- OpenRouter
- Ollama Cloud
- Google Gemini

## Model Hosting

- Hugging Face Hub

## Visualisation

- Streamlit
- Plotly

## Report Generation

- python-docx
- fpdf2

## Cloud Deployment

- Streamlit Community Cloud

---

# 📦 Application Dependencies

The Streamlit application currently uses packages such as:

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

The official list is stored in:

```text
requirements.txt
```

---

# 🔐 Streamlit Secrets

Sensitive credentials are not stored directly in GitHub.

The deployed system uses Streamlit Secrets.

Example configuration:

```toml
HF_MODEL_REPO = "YOUR_HUGGINGFACE_MODEL_REPOSITORY"
HF_TOKEN = "YOUR_HUGGINGFACE_READ_TOKEN"

OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
OPENROUTER_MODEL = "openrouter/free"

OLLAMA_API_KEY = "YOUR_OLLAMA_API_KEY"
OLLAMA_MODEL = "gpt-oss:20b"

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_MODEL = "YOUR_CONFIGURED_GEMINI_MODEL"
```

> Real tokens and API keys must never be committed to GitHub.

---

# 🚀 Running the Application Locally

## 1. Clone the repository

```bash
git clone <repository-url>
```

Then:

```bash
cd FYP-Brand-Reputation-System
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure credentials

Add the required:

- Hugging Face credentials;
- OpenRouter credentials;
- Ollama credentials;
- Gemini credentials.

---

## 4. Run Streamlit

```bash
streamlit run streamlit_app.py
```

---

# ☁️ Streamlit Community Cloud

Deployment configuration:

```text
Repository:
FYP-Brand-Reputation-System

Branch:
main

Main file:
streamlit_app.py
```

Required API credentials are configured through Streamlit Cloud Secrets.

---

# ✅ Final Functional Status

The major application components have been successfully implemented and tested.

```text
✅ Hugging Face DistilBERT loading

✅ Single Review prediction

✅ CSV upload

✅ XLSX upload

✅ Batch sentiment classification

✅ Brand Reputation Score

✅ Sentiment Distribution

✅ Customer Issue Analysis

✅ Customer Voice Analysis

✅ OpenRouter integration

✅ Ollama Cloud integration

✅ Gemini integration

✅ Technical Manager

✅ Product Manager

✅ Customer Service Manager

✅ Marketing Manager

✅ Subscription Manager

✅ Executive Manager

✅ Session-state report preservation

✅ Manager report regeneration handling

✅ Executive report invalidation handling

✅ Markdown report downloads

✅ Complete JSON export

✅ Microsoft Word report generation

✅ PDF report generation

✅ Professional Report Centre

✅ Multi-provider management architecture
```

---

# 🧪 Recommended Functional Test

| Test | Expected Result |
|---|---|
| Positive single review | Positive prediction |
| Negative single review | Negative prediction |
| Empty single review | Warning |
| CSV upload | Accepted |
| XLSX upload | Accepted |
| Missing review values | Safely ignored |
| Batch prediction | Predictions generated |
| Reputation dashboard | Indicators displayed |
| Sentiment distribution | Chart displayed |
| Issue analysis | Issue mentions shown |
| Customer voice | Word frequencies shown |
| Technical Manager | OpenRouter report generated |
| Product Manager | Ollama report generated |
| Customer Service Manager | OpenRouter report generated |
| Marketing Manager | Ollama report generated |
| Subscription Manager | OpenRouter report generated |
| Executive before 5 reports | Prevented |
| Executive after 5 reports | Gemini report generated |
| DOCX generation | Successful |
| PDF generation | Successful |
| New dataset | Previous AI reports cleared |
| Regenerated manager | Previous executive output cleared |

---

# 🎬 Recommended Demonstration Workflow

For the final FYP demonstration:

```text
1. Open BrandPulse AI
        ↓
2. Test Positive Single Review
        ↓
3. Test Negative Single Review
        ↓
4. Upload Representative CSV
        ↓
5. Run Batch Intelligence
        ↓
6. View Reputation Dashboard
        ↓
7. Explain Reputation Score
        ↓
8. Explain Issue Analysis
        ↓
9. Generate Technical Manager
        ↓
10. Generate Product Manager
        ↓
11. Generate Customer Service Manager
        ↓
12. Generate Marketing Manager
        ↓
13. Generate Subscription Manager
        ↓
14. Generate Executive Manager
        ↓
15. Generate DOCX + PDF
        ↓
16. Download Professional Report
```

A manageable representative dataset is recommended during the live demonstration to reduce cloud processing time.

---

# ⚠️ Known Limitations

## 1. Cloud Computing Resources

Streamlit Community Cloud has finite computational resources.

Very large datasets may require:

- significant CPU processing;
- memory;
- model inference time.

Large-scale model experimentation is therefore performed in Google Colab rather than through the deployed Streamlit interface.

---

## 2. Binary Sentiment Classification

The deployed DistilBERT model predicts:

```text
Positive
Negative
```

Neutral sentiment is not included in the final deployed binary workflow.

---

## 3. Issue Categorisation

Issue analysis currently uses predefined keyword-based rules.

Therefore:

- one review may match several categories;
- some alternative wording may not be detected;
- some reviews may remain Other or Unclear.

---

## 4. LLM Provider Availability

The system depends on external generative AI services.

OpenRouter, Ollama, or Gemini may temporarily experience:

- rate limits;
- service limits;
- model unavailability;
- network errors.

The multi-provider architecture reduces dependency on a single service but does not eliminate third-party service limitations.

---

## 5. OpenRouter Free Routing

The application requests:

```text
openrouter/free
```

The underlying model may therefore change according to availability.

BrandPulse AI displays the actual model returned where possible.

---

## 6. LLM Hallucination

Large Language Models may generate unsupported or inaccurate statements.

BrandPulse AI prompts instruct the LLMs to:

- use only supplied evidence;
- avoid inventing statistics;
- avoid inventing customer counts;
- avoid inventing business facts;
- clearly distinguish recommendations from observations;
- acknowledge insufficient evidence.

LLM reports should nevertheless be treated as **decision-support recommendations**, not independently verified facts.

---

## 7. Reputation Score Interpretation

The Brand Reputation Score is an internal project indicator.

It should not be interpreted as:

- an official Spotify metric;
- an industry-standard reputation index;
- a financial valuation;
- a universal brand-equity measure.

---

# 🔐 Security Considerations

Before publishing or sharing the repository:

- do not commit API keys;
- do not commit Hugging Face write tokens;
- do not include Gemini API keys;
- do not include OpenRouter API keys;
- do not include Ollama API keys;
- inspect notebooks for accidentally printed credentials;
- revoke any credential that has previously been exposed.

---

# 🔬 Academic Transparency

The repository separates the research experimentation stage from the final application.

```text
notebooks/
│
├── Model Development
├── Model Evaluation
├── Feature Representation
├── DistilBERT
└── Hybrid Experiments


src/
│
├── DistilBERT Prediction
├── Reputation Analytics
├── Multi-LLM Integration
└── Report Generation


streamlit_app.py
│
└── Final Interactive Decision-Support Application
```

This separation ensures that the Streamlit application demonstrates deployment of the selected model without replacing the experimental research process performed in Google Colab.

---

# 🔮 Future Improvements

Potential future development includes:

- high-capacity cloud inference;
- background batch processing;
- asynchronous review analysis;
- direct Google Play/App Store review collection;
- multilingual sentiment classification;
- topic modelling;
- transformer-based issue categorisation;
- multi-label issue classification;
- time-series reputation analysis;
- historical reputation tracking;
- competitor reputation comparison;
- retrieval-augmented generation;
- automatic LLM-grounding verification;
- LLM output quality scoring;
- database integration;
- authentication;
- management KPI monitoring;
- department-specific dashboards;
- automated scheduled reputation monitoring.

---

# 📊 Final Component Summary

| Component | Technology | Main Purpose |
|---|---|---|
| Review Input | Streamlit | Collect review text |
| Sentiment Classification | DistilBERT | Positive/Negative prediction |
| Model Hosting | Hugging Face | Host final transformer |
| Reputation Score | Python | Brand-level sentiment indicator |
| Issue Analysis | Python Rules | Detect recurring concerns |
| Customer Voice | Python | Identify recurring terms |
| Technical Manager | OpenRouter | Technical interpretation |
| Product Manager | Ollama `gpt-oss:20b` | Product interpretation |
| Customer Service Manager | OpenRouter | Service interpretation |
| Marketing Manager | Ollama `gpt-oss:20b` | Marketing interpretation |
| Subscription Manager | OpenRouter | Subscription interpretation |
| Executive Manager | Gemini | Consolidate all department reports |
| Visualisation | Streamlit + Plotly | Interactive dashboard |
| DOCX Export | python-docx | Editable professional report |
| PDF Export | fpdf2 | Fixed-format professional report |

---

# ✅ Final Project Status

```text
✅ Dataset Integration

✅ Text Preprocessing

✅ TF-IDF Experiments

✅ Embedding Experiments

✅ Traditional ML Experiments

✅ Deep Learning Experiments

✅ DistilBERT Experiment

✅ Hybrid Experiment

✅ Final DistilBERT Export

✅ Hugging Face Hosting

✅ Streamlit Deployment

✅ Single Review Intelligence

✅ Batch Review Intelligence

✅ Reputation Dashboard

✅ Brand Reputation Score

✅ Issue Analysis

✅ Customer Voice Analysis

✅ Multi-LLM Architecture

✅ OpenRouter Integration

✅ Ollama Cloud Integration

✅ Gemini Executive Integration

✅ Five Department Managers

✅ Executive Manager

✅ DOCX Report Generation

✅ PDF Report Generation

✅ Professional Report Centre

✅ Final End-to-End Application Workflow

🔄 Final System Evaluation

🔄 LLM Output Evaluation

🔄 Final FYP Documentation

🔄 Final Presentation Preparation
```

---

# ⚖️ Disclaimer

BrandPulse AI is an **academic Final Year Project prototype**.

The application demonstrates the integration of:

- NLP-based sentiment classification;
- brand reputation analytics;
- multi-provider Large Language Models;
- management decision-support reporting.

Generated sentiment predictions and management recommendations should not be interpreted as:

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

**Primary Predictive Model:**  
DistilBERT

**Sentiment Classes:**  
Positive and Negative

**Experimental Platform:**  
Google Colab

**Model Hosting:**  
Hugging Face Hub

**Application Framework:**  
Streamlit

**Deployment:**  
Streamlit Community Cloud

**Department LLM Providers:**  
OpenRouter and Ollama Cloud

**Executive LLM Provider:**  
Gemini

**Report Formats:**  
Microsoft Word (`.docx`) and PDF (`.pdf`)

---

# 📝 Final Summary

BrandPulse AI integrates three levels of intelligence:

```text
1. Predictive Intelligence
   │
   └── DistilBERT Sentiment Classification


2. Analytical Intelligence
   │
   ├── Brand Reputation Score
   ├── Sentiment Distribution
   ├── Customer Issue Analysis
   └── Customer Voice Intelligence


3. Generative Management Intelligence
   │
   ├── Technical Manager
   ├── Product Manager
   ├── Customer Service Manager
   ├── Marketing Manager
   ├── Subscription Manager
   └── Executive Manager
```

The experimental notebooks provide the modelling and evaluation foundation, while BrandPulse AI demonstrates how a selected NLP model can be deployed as an interactive **brand reputation decision-support system** combining predictive analytics, multi-LLM management interpretation, executive reporting, and professional document generation.
