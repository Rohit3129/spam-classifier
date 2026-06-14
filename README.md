markdown<div align="center">

# 📧 Email Spam Classifier

### ML-powered spam detection with a production-ready REST API

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Accuracy](https://img.shields.io/badge/Accuracy-98.4%25-2ECC71?style=for-the-badge)](/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> Classifies emails and SMS messages as **spam or not spam** using a TF-IDF + Naive Bayes pipeline — served through a clean, lightweight Flask REST API.

<br/>

[🚀 Quick Start](#-quick-start) •
[📡 API Docs](#-api-reference) •
[📊 Results](#-model-performance) •
[⚙️ How It Works](#%EF%B8%8F-how-it-works) •
[👤 Author](#-author)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Model Performance](#-model-performance)
- [How It Works](#%EF%B8%8F-how-it-works)
- [Dataset](#-dataset)
- [Author](#-author)

---

## 🧠 Overview

Spam detection is a classic NLP classification problem — but most implementations stop at the Jupyter notebook. This project goes further: a trained model serialised and deployed behind a REST API, ready to classify messages in real time.

Built with simplicity in mind. No overengineering. Just a well-tuned pipeline that works.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🎯 High Accuracy | 98.4% accuracy on holdout test set |
| ⚡ Fast Inference | Sub-100ms response via REST API |
| 🧹 Text Preprocessing | Lowercasing, stopword removal, stemming |
| 📦 Serialised Model | Pickle-based model + vectorizer persistence |
| 🔌 REST API | Clean JSON interface via Flask |
| 📓 Full EDA | Exploration notebook with confusion matrix & ROC curve |

---

## 📁 Project Structure
email-spam-classifier/

│

├── 📂 model/

│   ├── train.py              # Training pipeline

│   ├── model.pkl             # Serialised Naive Bayes classifier

│   └── vectorizer.pkl        # Fitted TF-IDF vectorizer

│

├── 📂 api/

│   └── app.py                # Flask REST API

│

├── 📂 data/

│   └── spam.csv              # UCI SMS Spam Collection (5,574 messages)

│

├── 📂 notebooks/

│   └── exploration.ipynb     # EDA, model benchmarks, confusion matrix

│

├── requirements.txt

└── README.md

---

## 🚀 Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/Rohit3129/email-spam-classifier
cd email-spam-classifier
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Train the model**
```bash
python model/train.py
# Outputs: model/model.pkl + model/vectorizer.pkl
```

**4. Start the API**
```bash
python api/app.py
# Running on http://localhost:5000
```

**5. Test it**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You have won a free iPhone. Click here now."}'
```

```json
{
  "prediction": "spam",
  "confidence": 0.97
}
```

<p align="right"><a href="#-table-of-contents">↑ Back to top</a></p>

---

## 📡 API Reference

### `POST /predict`

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `string` | ✅ | The email or SMS text to classify |

**Example Request**
```json
{
  "message": "Your account has been compromised. Verify now at http://scam.com"
}
```

**Example Response**
```json
{
  "prediction": "spam",
  "confidence": 0.96
}
```

---

### `GET /health`

```bash
curl http://localhost:5000/health
# {"status": "ok"}
```

<p align="right"><a href="#-table-of-contents">↑ Back to top</a></p>

---

## 📊 Model Performance

Evaluated on a stratified 80/20 train-test split.

| Metric | Score |
|--------|-------|
| ✅ Accuracy | **98.4%** |
| 🎯 Precision | **97.1%** |
| 🔁 Recall | **96.8%** |
| ⚖️ F1 Score | **96.9%** |

Full evaluation report, confusion matrix, and ROC curve in [`notebooks/exploration.ipynb`](notebooks/exploration.ipynb)

---

## ⚙️ How It Works
Raw Text

│

▼

Preprocessing (lowercase → remove stopwords → stem)

│

▼

TF-IDF Vectorization  (converts text → sparse feature matrix)

│

▼

Multinomial Naive Bayes  (trained on 80% of dataset)

│

▼

Prediction + Confidence Score

**Why Naive Bayes over SVM / Logistic Regression?**

All three were benchmarked. Naive Bayes matched both in accuracy while training significantly faster and handling sparse TF-IDF vectors more naturally. Right tradeoff for this scale.

<p align="right"><a href="#-table-of-contents">↑ Back to top</a></p>

---

## 📦 Tech Stack
Python 3.10       →  Core language

Scikit-learn      →  Model training + TF-IDF vectorization

NLTK              →  Text preprocessing

Flask             →  REST API

Pickle            →  Model serialization

Pandas / NumPy    →  Data handling

---

## 🗂️ Dataset

**UCI SMS Spam Collection**
- 5,574 labelled messages
- 86.6% ham / 13.4% spam
- [View dataset →](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)

---

## 👤 Author

**Rohit Lamkhade** — MSc Advanced Computer Science, Swansea University UK

[![GitHub](https://img.shields.io/badge/GitHub-Rohit3129-181717?style=flat-square&logo=github)](https://github.com/Rohit3129)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-rohit--lamkhade-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/rohit-lamkhade-243ab2283)
[![Email](https://img.shields.io/badge/Email-rohitlamkhade301%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:rohitlamkhade301@gmail.com)

---

<div align="center">

If this was useful, drop a ⭐ — it helps others find it.

</div>
