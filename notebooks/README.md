# 📓 BrandPulse AI — Experimental Notebooks

## Online Review-Based Brand Reputation Prediction Using NLP Techniques

This folder contains the Google Colab notebooks used for the data preparation, model development, experimentation, evaluation, and deployment preparation of the **BrandPulse AI Final Year Project (FYP)**.

The project focuses on analysing **Spotify application reviews** using Natural Language Processing (NLP) techniques to predict customer sentiment and support brand reputation analysis.

Three main experimental notebooks are included:

```text
notebooks/
│
├── FYP_Single_Algorithm.ipynb
├── FYP_DistilBERT.ipynb
├── FYP_Hybrid.ipynb
└── README.md
```

Each notebook serves a different purpose within the overall experimental workflow.

> **Important:** The notebooks are related to one another and are not completely independent. The complete text preprocessing workflow is performed in `FYP_Single_Algorithm.ipynb`. The DistilBERT and Hybrid notebooks primarily load the preprocessed datasets that were previously saved as CSV/XLSX files.

---

# 📌 Notebook Overview

| Notebook | Main Purpose | Full Preprocessing Included? | Deployment Status |
|---|---|---:|---|
| `FYP_Single_Algorithm.ipynb` | Data preprocessing, feature representation, and individual model experiments | ✅ Yes | Experimental |
| `FYP_DistilBERT.ipynb` | DistilBERT fine-tuning, evaluation, and model export | ❌ No | ✅ Current deployed sentiment model |
| `FYP_Hybrid.ipynb` | Hybrid modelling and combination experiments | ❌ No | Experimental |

The overall relationship between the notebooks is:

```text
Original Spotify Review Datasets
              │
              ▼
FYP_Single_Algorithm.ipynb
              │
              ├── Dataset Integration
              ├── Full Text Preprocessing
              ├── Feature Representation
              ├── Individual Model Experiments
              │
              ▼
      Saved CSV / XLSX Files
              │
       ┌──────┴────────┐
       │               │
       ▼               ▼
FYP_DistilBERT     FYP_Hybrid
    .ipynb           .ipynb
       │               │
       ▼               ▼
DistilBERT Model    Hybrid Experiments
       │
       ▼
Hugging Face
       │
       ▼
BrandPulse AI
Streamlit System
```

---

# 📊 Dataset Sources

The project uses Spotify review datasets obtained from **Kaggle**.

The datasets are used for academic research and model-development purposes. Users reproducing the project should download the required datasets directly from their original Kaggle sources and follow the respective dataset licences and terms of use.

## Dataset 1 — Top 20 Play Store App Reviews Daily Update

Spotify review file:

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

# 🔄 General Experimental Workflow

The notebooks approximately follow this workflow:

```text
Kaggle Spotify Review Datasets
              │
              ▼
       Dataset Integration
              │
              ▼
       Data Exploration
              │
              ▼
       Text Preprocessing
              │
              ▼
    Save Processed Datasets
              │
              ▼
     Data Splitting / Labels
              │
              ▼
     Feature Representation
              │
              ▼
       Model Development
              │
              ▼
      Validation / Testing
              │
              ▼
       Model Comparison
              │
              ▼
     Final Model Selection
              │
              ▼
        Model Deployment
```

The **full preprocessing stage is only implemented in `FYP_Single_Algorithm.ipynb`**.

The other notebooks reuse the preprocessed datasets saved by the earlier workflow.

---

# 1️⃣ FYP_Single_Algorithm.ipynb

## Purpose

`FYP_Single_Algorithm.ipynb` is the main notebook for:

- Dataset preparation;
- Full text preprocessing;
- Data exploration;
- Feature representation;
- Individual machine-learning experiments;
- Deep-learning experiments;
- Model comparison.

This notebook should normally be executed **first** when reproducing the complete project workflow.

---

## Full Text Preprocessing

The complete text preprocessing pipeline is implemented in this notebook.

The preprocessing stage prepares the raw Spotify reviews before they are used for model development.

The workflow includes operations such as:

- Text normalisation;
- Lowercasing;
- Contraction expansion;
- Slang and abbreviation normalisation;
- Spelling-related normalisation;
- Repeated-character normalisation;
- Repeated-punctuation handling;
- URL removal;
- HTML removal;
- Mention handling;
- Hashtag normalisation;
- Emoji handling;
- Language filtering;
- Duplicate removal;
- Short-review handling;
- Creation of processed review datasets.

The processed datasets are then saved for reuse by the DistilBERT and Hybrid notebooks.

---

## Why Preprocessing Is Not Repeated in Every Notebook

The preprocessing pipeline is intentionally centralised in the Single Algorithm notebook.

Instead of performing the same preprocessing multiple times:

```text
Single Algorithm
→ Full preprocessing

DistilBERT
→ Full preprocessing again

Hybrid
→ Full preprocessing again
```

the project uses:

```text
Single Algorithm
        │
        ▼
Full preprocessing
        │
        ▼
Save processed datasets
        │
        ├─────────────► DistilBERT
        │
        └─────────────► Hybrid
```

This reduces unnecessary repetition and helps ensure that different modelling experiments use consistent processed data.

---

## Feature Representation Experiments

This notebook contains experiments involving different feature representations.

These may include:

```text
TF-IDF
│
├── Unigram
├── Unigram + Bigram
└── Unigram + Bigram + Trigram


Embedding Representations
│
├── Word2Vec
├── GloVe
└── FastText
```

Different model and feature-representation combinations are evaluated to determine their performance for Spotify review sentiment classification.

---

## Model Experiments

The Single Algorithm notebook contains individual model experiments such as traditional machine-learning and deep-learning approaches.

The exact models used depend on the experimental configuration within the notebook.

The purpose of these experiments is to compare different combinations before selecting models for further analysis and deployment.

---

## Saved Processed Files

After preprocessing, datasets are saved in formats such as:

```text
.csv
.xlsx
```

Examples may include files such as:

```text
spotify_reviews_preprocessed.csv

spotify_reviews_tfidf_dataset.xlsx

spotify_reviews_embedding_dataset.xlsx
```

> The exact filenames and paths may differ depending on the version of the notebook and Google Drive directory used during experimentation.

These saved datasets are later loaded by the DistilBERT and Hybrid notebooks.

---

# 2️⃣ FYP_DistilBERT.ipynb

## Purpose

`FYP_DistilBERT.ipynb` contains the transformer-based sentiment-classification experiment using **DistilBERT**.

The final BrandPulse AI Streamlit application currently uses the DistilBERT model produced by this workflow for sentiment prediction.

---

## Important Preprocessing Note

This notebook **does not contain the complete text preprocessing pipeline**.

Instead, it loads a dataset that has already been prepared and saved by the earlier preprocessing workflow.

Therefore:

```text
FYP_Single_Algorithm.ipynb
              │
              ▼
      Full Preprocessing
              │
              ▼
      Saved CSV / XLSX
              │
              ▼
FYP_DistilBERT.ipynb
```

Before running the DistilBERT notebook, make sure the required processed dataset exists at the configured path.

---

## Main DistilBERT Workflow

The notebook includes tasks related to:

- loading the saved processed dataset;
- preparing sentiment labels;
- creating training, validation, and testing datasets;
- tokenising customer reviews;
- configuring DistilBERT;
- preparing class weights;
- training/fine-tuning the model;
- validation;
- testing;
- calculating evaluation metrics;
- generating classification results;
- generating confusion matrices;
- saving the final model;
- saving the tokenizer;
- preparing the model for Hugging Face deployment.

---

## Binary Sentiment Classification

The final deployed DistilBERT model performs binary sentiment classification:

```text
0 → Negative
1 → Positive
```

The trained model configuration also stores the corresponding label mappings.

---

## Model Export

After training and evaluation, the final model and tokenizer are saved.

Typical exported files may include:

```text
config.json
model.safetensors
tokenizer_config.json
special_tokens_map.json
vocab.txt
```

The model is then uploaded to a Hugging Face model repository.

---

## Relationship with Streamlit

The deployed workflow is:

```text
FYP_DistilBERT.ipynb
        │
        ▼
Train Final DistilBERT
        │
        ▼
Save Model + Tokenizer
        │
        ▼
Upload to Hugging Face
        │
        ▼
Streamlit Cloud
        │
        ▼
BrandPulse AI
```

The Streamlit application downloads the saved DistilBERT model and tokenizer from Hugging Face and uses them for review sentiment prediction.

---

# 3️⃣ FYP_Hybrid.ipynb

## Purpose

`FYP_Hybrid.ipynb` contains experiments related to the hybrid modelling stage of the project.

The notebook is used to investigate whether combining selected model outputs or representations can improve sentiment-classification performance.

The Hybrid notebook is retained as part of the project's experimental comparison but is **not currently used as the deployed Streamlit sentiment model**.

---

## Important Preprocessing Note

Similar to the DistilBERT notebook, the Hybrid notebook does **not repeat the complete preprocessing workflow**.

Instead, it uses the previously saved processed datasets.

```text
FYP_Single_Algorithm.ipynb
             │
             ▼
     Processed Dataset
             │
             ▼
      CSV / XLSX Files
             │
             ▼
    FYP_Hybrid.ipynb
```

The required dataset paths must therefore be valid before executing the Hybrid notebook.

---

## Hybrid Workflow

Depending on the experimental configuration, the notebook may include:

- Loading saved processed datasets;
- Loading selected feature representations;
- Loading or training selected models;
- Generating model predictions;
- Combining selected prediction outputs;
- Implementing hybrid or fusion approaches;
- Evaluating hybrid results;
- Comparing hybrid and individual-model performance.

---

# 🗂 Recommended Notebook Execution Order

For users who want to reproduce the project from the beginning, the recommended order is:

## Step 1 — Single Algorithm Notebook

Run:

```text
FYP_Single_Algorithm.ipynb
```

Main workflow:

```text
Download / Prepare Raw Datasets
              ↓
Integrate Spotify Reviews
              ↓
Run Full Text Preprocessing
              ↓
Prepare Labels / Data
              ↓
Run Individual Experiments
              ↓
Save Processed CSV / XLSX Files
```

---

## Step 2 — DistilBERT Notebook

Run:

```text
FYP_DistilBERT.ipynb
```

Main workflow:

```text
Load Saved Processed Dataset
              ↓
Prepare DistilBERT Dataset
              ↓
Tokenisation
              ↓
Fine-Tuning
              ↓
Validation
              ↓
Testing
              ↓
Save Final Model
              ↓
Upload to Hugging Face
```

---

## Step 3 — Hybrid Notebook

Run:

```text
FYP_Hybrid.ipynb
```

Main workflow:

```text
Load Saved Processed Dataset(s)
              ↓
Load / Train Selected Components
              ↓
Generate Predictions
              ↓
Hybrid / Fusion Method
              ↓
Evaluate Results
              ↓
Compare with Individual Models
```

---

# ☁️ Google Colab Environment

The notebooks were primarily developed and executed using **Google Colab**.

Some cells mount Google Drive using:

```python
from google.colab import drive

drive.mount(
    "/content/drive"
)
```

After mounting Google Drive, files are accessed through paths such as:

```text
/content/drive/MyDrive/...
```

---

# ⚠️ Important Google Drive Path Requirement

Some notebook code is based on the **original Google Drive folder structure used during project development**.

For example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "spotify_preprocessed_output/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

This path may not exist when another user runs the notebook.

The user must modify the file path according to their own Google Drive structure.

For example:

```python
DATASET_PATH = (
    "/content/drive/MyDrive/"
    "FYP/data/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

The same applies to paths used for:

- raw datasets;
- preprocessed datasets;
- CSV files;
- XLSX files;
- model checkpoints;
- saved model folders;
- exported predictions;
- validation results;
- testing results;
- Hugging Face deployment folders.

---

# 🛠 How to Modify the Google Drive Paths

Suppose the notebook contains:

```python
TFIDF_DATASET_PATH = (
    "/content/drive/MyDrive/"
    "spotify_preprocessed_output/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

but the actual file is stored at:

```text
MyDrive/FYP/Datasets/spotify_reviews_tfidf_dataset.xlsx
```

change the code to:

```python
TFIDF_DATASET_PATH = (
    "/content/drive/MyDrive/"
    "FYP/Datasets/"
    "spotify_reviews_tfidf_dataset.xlsx"
)
```

Always confirm that:

```text
folder name
+
filename
+
file extension
```

match the actual file in Google Drive.

---

# ❌ FileNotFoundError

A common error when reproducing these notebooks is:

```text
FileNotFoundError:
[Errno 2] No such file or directory
```

This usually indicates that the configured file path does not exist in the current environment.

For example:

```text
/content/drive/MyDrive/
spotify_preprocessed_output/
spotify_reviews_tfidf_dataset.xlsx
```

may exist in the original project Drive but not in another Google account.

---

## Checking Google Drive Files

After mounting Google Drive, users can inspect their folders using:

```python
import os

print(
    os.listdir(
        "/content/drive/MyDrive"
    )
)
```

For a specific directory:

```python
import os

folder_path = (
    "/content/drive/MyDrive/FYP"
)

print(
    os.listdir(
        folder_path
    )
)
```

Then update the notebook path accordingly.

---

# 💾 CSV and XLSX Dependency

The DistilBERT and Hybrid notebooks may load saved files such as:

```text
.csv
.xlsx
```

These files are expected to have been created previously.

Therefore, if the notebook attempts to load:

```python
pd.read_csv(...)
```

or:

```python
pd.read_excel(...)
```

and the required file has not been created yet, users should first run the relevant preprocessing/export sections of:

```text
FYP_Single_Algorithm.ipynb
```

---

# 📌 Reproducibility Relationship

The notebooks should be understood as a connected experimental pipeline:

```text
                 RAW DATASETS
                      │
                      ▼
          FYP_Single_Algorithm.ipynb
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Preprocessing   Experiments   Saved Files
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                          ▼                   ▼
                 FYP_DistilBERT       FYP_Hybrid
                      │                   │
                      ▼                   ▼
                  Transformer          Hybrid
                   Modelling          Modelling
                      │
                      ▼
                Final DistilBERT
                      │
                      ▼
                  Hugging Face
                      │
                      ▼
                  BrandPulse AI
```

This design helps prevent differences caused by independently preprocessing the same reviews in multiple notebooks.

---

# 🔬 Experimental Model vs Deployed Model

Several models and feature representations are investigated during the experimental stage.

However, the current Streamlit application uses:

```text
DistilBERT
```

as its deployed sentiment-classification model.

The notebooks therefore serve different purposes:

| Notebook | Role |
|---|---|
| Single Algorithm | Preprocessing and individual modelling experiments |
| DistilBERT | Transformer modelling and deployment |
| Hybrid | Hybrid/fusion experimentation |

The presence of an experiment in the repository does not necessarily mean that model is used by the final Streamlit system.

---

# 🌐 Relationship with BrandPulse AI

The notebooks are primarily responsible for the **model-development layer**.

The main repository outside this folder contains the final application and decision-support components.

```text
Experimental Notebooks
        │
        ▼
Model Training and Evaluation
        │
        ▼
Final DistilBERT Model
        │
        ▼
Hugging Face
        │
        ▼
BrandPulse AI
        │
        ├── Single Review Prediction
        ├── Batch Review Analysis
        ├── Reputation Dashboard
        ├── Customer Issue Analysis
        ├── Customer Voice Analysis
        ├── AI Management Council
        └── Executive Reporting
```

The LLM management components are part of the Streamlit application and are separate from the experimental modelling notebooks.

---

# 🤖 Generative AI Is Not Used for Sentiment Prediction

The final system separates predictive NLP and generative AI.

```text
DistilBERT
│
└── Sentiment Prediction


Analytics Layer
│
├── Sentiment Distribution
├── Brand Reputation Score
├── Issue Analysis
└── Customer Voice Analysis


LLM Layer
│
├── Technical Manager
├── Product Manager
├── Customer Service Manager
├── Marketing Manager
├── Subscription Manager
└── Executive Manager
```

Gemini and OpenRouter are therefore used to interpret existing analytical evidence and generate management recommendations rather than replacing the trained DistilBERT sentiment model.

---

# 🔐 Security and API Credentials

Do not commit real API tokens or keys to these notebooks.

Examples of information that should **not** appear directly inside notebook cells include:

```python
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxx"

GEMINI_API_KEY = "xxxxxxxxxxxxxxxx"

OPENROUTER_API_KEY = "xxxxxxxxxxxxxxxx"
```

Sensitive credentials should be stored using secure environment variables, notebook authentication mechanisms, or Streamlit Secrets.

If a real token or API key is accidentally committed to GitHub, revoke the exposed credential and create a new one.

---

# 💻 Computational Requirements

Some notebook experiments can require significant computational resources.

This is especially relevant for:

- LSTM;
- BiLSTM;
- CNN;
- embedding-based experiments;
- transformer fine-tuning;
- DistilBERT;
- large datasets.

GPU acceleration is recommended for deep-learning and transformer experiments.

Google Colab resource availability may vary depending on the runtime and account.

---

# ⚠️ Out-of-Memory Errors

Large model training can cause errors such as:

```text
OutOfMemoryError
```

If this occurs, possible adjustments include:

- reducing training batch size;
- reducing evaluation batch size;
- clearing unused GPU variables;
- restarting the Colab runtime;
- training the transformer in a separate notebook/runtime;
- reducing sequence length when appropriate.

These adjustments should be made carefully because changes to training configuration may affect experimental comparability.

---

# 📦 Library Versions

Notebook results may be affected by changes in Python package versions.

Relevant libraries may include:

```text
pandas
numpy
scikit-learn
torch
transformers
gensim
tensorflow / keras
imbalanced-learn
openpyxl
```

If older notebook code produces errors after a package update, check the installed package version before modifying the experimental methodology.

For example:

```python
import transformers

print(
    transformers.__version__
)
```

---

# 🔁 Reproducibility Notes

Exact results may vary slightly between executions due to factors such as:

- random initialisation;
- GPU behaviour;
- package versions;
- model initialisation;
- data splitting;
- random seed;
- deep-learning training behaviour.

Where random seeds are used in the notebooks, they should be preserved when attempting to reproduce the original experiments.

---

# 📊 Model Evaluation

Model evaluation is performed within the experimental notebooks rather than through the Streamlit visualisation layer.

Evaluation may include metrics such as:

```text
Accuracy
Precision
Recall
F1-Score
Confusion Matrix
```

Validation results are used during model development and selection, while final testing should be performed using data that was not used to train the selected model.

---

# 📂 Suggested Folder Structure in Google Drive

Users reproducing the project may organise Google Drive using a structure such as:

```text
MyDrive/
│
└── FYP/
    │
    ├── raw_data/
    │
    ├── preprocessed_data/
    │
    ├── tfidf_data/
    │
    ├── embedding_data/
    │
    ├── models/
    │
    ├── results/
    │
    └── exports/
```

Notebook paths can then be updated accordingly.

For example:

```python
BASE_PATH = (
    "/content/drive/MyDrive/FYP"
)

RAW_DATA_PATH = (
    f"{BASE_PATH}/raw_data"
)

PREPROCESSED_PATH = (
    f"{BASE_PATH}/preprocessed_data"
)

MODEL_PATH = (
    f"{BASE_PATH}/models"
)
```

This is only an example structure. It does not need to match the original project paths.

---

# ✅ Recommended Reproduction Checklist

Before running the notebooks, check the following:

- [ ] Required Kaggle datasets have been downloaded.
- [ ] Google Drive has been mounted.
- [ ] File paths have been updated.
- [ ] Required Python packages are installed.
- [ ] The Single Algorithm notebook is available.
- [ ] Full preprocessing has been completed before running dependent notebooks.
- [ ] Required CSV/XLSX files exist.
- [ ] DistilBERT notebook points to the correct processed dataset.
- [ ] Hybrid notebook points to the correct processed dataset(s).
- [ ] GPU runtime is enabled when required.
- [ ] No API keys are hard-coded in the notebook.
- [ ] Export directories exist before saving files.

---

# 📚 Dataset Attribution

The datasets used in this project were obtained from Kaggle.

### 1. Top 20 Play Store App Reviews Daily Update

https://www.kaggle.com/datasets/odins0n/top-20-play-store-app-reviews-daily-update?select=Spotify.csv

### 2. App Store Music App Reviews

https://www.kaggle.com/datasets/cluesec/app-store-music-app-reviews

### 3. Top 10 Global Apps Play Store Reviews

https://www.kaggle.com/datasets/nitinchoudhary012/top-10-global-apps-play-store-reviews

### 4. Spotify App Reviews 2022

https://www.kaggle.com/datasets/mfaaris/spotify-app-reviews-2022

Users should refer to each Kaggle dataset page for the original creator information, licensing conditions, and latest dataset details.

---

# ⚠️ Important Notes for Repository Users

## 1. Full preprocessing is not repeated

The complete preprocessing workflow is located in:

```text
FYP_Single_Algorithm.ipynb
```

The DistilBERT and Hybrid notebooks load previously prepared data.

---

## 2. Google Drive paths must be modified

Paths such as:

```text
/content/drive/MyDrive/...
```

reflect the original Google Drive environment used during development.

They are **not guaranteed to work on another Google account**.

---

## 3. Saved preprocessing files are required

The DistilBERT and Hybrid notebooks may fail with:

```text
FileNotFoundError
```

if the required CSV/XLSX files have not been generated or are stored at a different location.

---

## 4. Not every experimental model is deployed

The repository contains multiple modelling experiments.

The final BrandPulse AI application currently deploys **DistilBERT** for sentiment prediction.

---

## 5. Large experiments may require GPU resources

Deep-learning and transformer experiments may be difficult to run using CPU-only environments.

---

# 🔮 Potential Future Improvements

Possible improvements to the experimental notebook workflow include:

- Centralising dataset paths in one configuration cell;
- Automatically validating required input files;
- Adding package-version information;
- Exporting experiment configurations automatically;
- Adding clearer experiment identifiers;
- Automatically saving model metrics;
- Integrating experiment tracking;
- Reducing repeated code between experiments;
- Creating a separate preprocessing notebook;
- Improving model reproducibility;
- Adding automated deployment preparation.

---

# 📄 Final Year Project Information

**Project Title:**  
Online Review-Based Brand Reputation Prediction Using NLP Techniques

**System Name:**  
BrandPulse AI

**Application Domain:**  
Spotify Customer Reviews

**Notebook Platform:**  
Google Colab

**Primary Deployed Sentiment Model:**  
DistilBERT

**Model Hosting:**  
Hugging Face

**Cloud Visualisation:**  
Streamlit Community Cloud

**Generative AI Providers:**  
Gemini and OpenRouter

---

# 📝 Summary

The notebooks in this folder should be understood as a connected model-development workflow rather than three completely independent notebooks.

The most important relationship is:

```text
FYP_Single_Algorithm.ipynb
        │
        │
        ├── Full Text Preprocessing
        ├── Individual Model Experiments
        │
        ▼
Saved Preprocessed CSV / XLSX Files
        │
        ├─────────────────────┐
        │                     │
        ▼                     ▼
FYP_DistilBERT.ipynb    FYP_Hybrid.ipynb
        │                     │
        ▼                     ▼
Transformer Modelling    Hybrid Modelling
        │
        ▼
Final DistilBERT Model
        │
        ▼
Hugging Face
        │
        ▼
BrandPulse AI
```

Users reproducing the work should therefore:

1. Update all Google Drive paths;
2. Run or obtain the preprocessing outputs from the Single Algorithm notebook;
3. Ensure the required CSV/XLSX files exist;
4. Run the DistilBERT and/or Hybrid experiments using those saved files;
5. Avoid placing sensitive API credentials directly in notebook code.

This structure helps maintain consistency between the different modelling experiments while keeping the preprocessing workflow centralised.
