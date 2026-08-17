# 🎧 BrandPulse AI
## Online Review-Based Brand Reputation Prediction Using NLP Techniques

BrandPulse AI is a Final Year Project (FYP) that applies Natural Language Processing (NLP), machine learning, transformer-based sentiment classification, and Large Language Models (LLMs) to analyse online customer reviews and transform them into brand reputation intelligence.

The current implementation focuses on **Spotify application reviews**. A trained **DistilBERT sentiment classification model** predicts whether customer reviews are positive or negative. The prediction results are then processed into brand reputation indicators, issue categories, customer-voice insights, and department-specific management recommendations.

The system is deployed as a cloud-based interactive dashboard using **Streamlit Community Cloud**.

---

# 📌 Project Overview

Traditional sentiment analysis mainly determines whether a customer opinion is positive or negative. BrandPulse AI extends this approach by converting sentiment predictions into information that can support management decision-making.

The system consists of three main intelligence layers:

1. **Predictive Intelligence**
   - DistilBERT sentiment classification
   - Positive and negative review prediction
   - Prediction confidence

2. **Brand Reputation Analytics**
   - Sentiment distribution
   - Brand Reputation Score
   - Customer issue categorisation
   - Frequent positive and negative terms
   - Reviews requiring management attention

3. **Generative AI Management Intelligence**
   - Department-specific AI managers
   - Evidence-based management recommendations
   - Executive-level report consolidation

---

# 🎯 Project Objectives

The objectives of BrandPulse AI are to:

- classify Spotify customer reviews using NLP techniques;
- identify positive and negative customer sentiment;
- transform sentiment predictions into brand-level reputation indicators;
- identify common customer issues from negative reviews;
- provide different management departments with relevant customer insights;
- generate evidence-based improvement recommendations using LLMs;
- consolidate department-level recommendations into an executive report;
- provide an interactive cloud-based visualisation platform.

---

# 🧠 System Architecture

```text
                    Customer Reviews
                          │
                          ▼
                 Streamlit Cloud App
                          │
                          ▼
                    DistilBERT Model
                  Hosted on Hugging Face
                          │
                          ▼
              Positive / Negative Prediction
                          │
                          ▼
               Brand Reputation Analytics
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
    Reputation Score   Issue Analysis   Customer Voice
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                AI Management Council
                          │
       ┌──────────────────┼────────────────────┐
       │                  │                    │
       ▼                  ▼                    ▼
   Gemini Managers   OpenRouter Managers   Department Reports
       │                  │                    │
       └──────────────────┼────────────────────┘
                          │
                          ▼
                   Executive Manager
                          │
                          ▼
             Executive Reputation Report
                          │
                          ▼
                  DOCX / PDF Export
