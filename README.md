Email Spam Classifier

A machine learning model that classifies emails as spam or not spam, served through a REST API. Trained on the UCI SMS Spam Collection dataset, hits 98%+ accuracy on the test set.


What it does

Takes an email/message as input, returns whether it's spam or not. That's it. No overcomplicated pipeline — just a clean TF-IDF + Naive Bayes model behind a Flask API.


Tech


Python, Scikit-learn, NLTK
Flask (REST API)
TF-IDF Vectorizer
Multinomial Naive Bayes



Project Structure

email-spam-classifier/
├── model/
│   ├── train.py          # training script
│   ├── model.pkl         # saved model
│   └── vectorizer.pkl    # saved TF-IDF vectorizer
├── api/
│   └── app.py            # Flask API
├── data/
│   └── spam.csv          # UCI dataset
├── notebooks/
│   └── exploration.ipynb # EDA + model experiments
├── requirements.txt
└── README.md


Getting started

bashgit clone https://github.com/Rohit3129/email-spam-classifier
cd email-spam-classifier
pip install -r requirements.txt

Train the model:

bashpython model/train.py

Run the API:

bashpython api/app.py

API runs on http://localhost:5000 by default.


API

POST /predict

Request:

json{
  "message": "Congratulations! You've won a free iPhone. Click here to claim."
}

Response:

json{
  "prediction": "spam",
  "confidence": 0.97
}

GET /health — sanity check, returns 200 OK


Model performance

MetricScoreAccuracy98.4%Precision97.1%Recall96.8%F1 Score96.9%

Evaluated on a 80/20 train-test split. Confusion matrix and full evaluation in notebooks/exploration.ipynb.


Why Naive Bayes

Tried logistic regression and SVM too. Naive Bayes won on this dataset — faster to train, comparable accuracy, and works well with sparse TF-IDF vectors. For a text classification problem at this scale it's the right call.


Dataset

UCI SMS Spam Collection — 5,574 messages, 13.4% spam.


Requirements

flask
scikit-learn
nltk
pandas
numpy


Author

Rohit Lamkhade — GitHub · LinkedIn
