

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            confusion_matrix, classification_report, roc_auc_score,
                            roc_curve, auc)
import pickle
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("ADVANCED EMAIL SPAM CLASSIFIER - PRODUCTION READY")
print("=" * 80)


# PHASE 1: DATA COLLECTION & PREPROCESSING


print("\n[PHASE 1] DATA COLLECTION & PREPROCESSING")


# Enhanced dataset with more examples
emails_data = {
    'email': [
        # Spam emails
        'Buy viagra online now!!! Click here!!!',
        'You won $1,000,000!!! Claim prize immediately',
        'FREE MONEY!!! Limited time offer!!!',
        'Click here to double your income NOW',
        'Congratulations! You are a winner! Claim prize',
        'URGENT: Verify your account immediately',
        'Work from home and earn $5000/week',
        'Hot singles in your area waiting',
        'Get rich quick with our secret method',
        'LIMITED TIME: 50% OFF EVERYTHING!!!',
        'Nigerian prince needs your help urgently',
        'Act now! This offer expires today!',
        'Unbelievable! Click to see results',
        'Best investment opportunity ever',
        'Your bank account needs verification NOW',
        
        # Legitimate emails
        'Hi, the meeting is scheduled for 3pm tomorrow',
        'Project deadline has been extended to Friday',
        'Please review the attached document',
        'Thank you for your collaboration on this project',
        'Can we reschedule our call to 2pm?',
        'The quarterly report is ready for review',
        'Please submit your timesheet by EOD',
        'Meeting notes from today are attached',
        'Welcome to the team! Looking forward to working together',
        'Your performance review is scheduled for next week',
        'Team lunch will be at 12pm on Friday',
        'Please find the budget spreadsheet attached',
        'Great work on the presentation yesterday',
        'The client approved the proposal',
        'Can you send me the project files?',
    ],
    'label': [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
}

df = pd.DataFrame(emails_data)
print(f"✓ Loaded {len(df)} emails")
print(f"✓ Spam: {(df['label'] == 1).sum()} | Legitimate: {(df['label'] == 0).sum()}")

# Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = ' '.join(text.split())
    return text

df['email_cleaned'] = df['email'].apply(preprocess_text)


# PHASE 2: FEATURE ENGINEERING WITH ADVANCED TECHNIQUES


print("\n[PHASE 2] FEATURE ENGINEERING")


# TF-IDF Vectorization with optimization
tfidf = TfidfVectorizer(
    max_features=100,
    stop_words='english',
    lowercase=True,
    min_df=1,
    max_df=0.95,
    ngram_range=(1, 2)  # Unigrams and bigrams
)

X = tfidf.fit_transform(df['email_cleaned'])
y = df['label']

print(f"✓ Feature matrix shape: {X.shape}")
print(f"✓ Top 15 important features:")
feature_names = tfidf.get_feature_names_out()
for i, name in enumerate(feature_names[:15]):
    print(f"   {i+1}. {name}")


# PHASE 3: TRAIN-TEST SPLIT WITH STRATIFICATION


print("\n[PHASE 3] TRAIN-TEST SPLIT")


X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.25,
    random_state=42,
    stratify=y
)

print(f"✓ Training set: {X_train.shape[0]} emails")
print(f"✓ Testing set: {X_test.shape[0]} emails")
print(f"✓ Training spam ratio: {y_train.sum() / len(y_train):.1%}")
print(f"✓ Testing spam ratio: {y_test.sum() / len(y_test):.1%}")


# PHASE 4: TRAIN MULTIPLE MODELS


print("\n[PHASE 4] TRAINING MULTIPLE MODELS")


models = {
    'Naive Bayes': MultinomialNB(),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='linear', probability=True, random_state=42)
}

trained_models = {}
cross_val_scores = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    
    # Train model
    model.fit(X_train, y_train)
    trained_models[name] = model
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    cross_val_scores[name] = cv_scores
    
    print(f"  ✓ Cross-validation F1: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")


# PHASE 5: MODEL EVALUATION & COMPARISON


print("\n[PHASE 5] MODEL EVALUATION & COMPARISON")
print("-" * 80)

results = {}

for name, model in trained_models.items():
    print(f"\n{name}:")
    
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = None
    try:
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    except:
        y_pred_proba = None
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'cv_score': cross_val_scores[name].mean()
    }
    
    print(f"  Accuracy:  {accuracy:.1%}")
    print(f"  Precision: {precision:.1%}")
    print(f"  Recall:    {recall:.1%}")
    print(f"  F1-Score:  {f1:.1%}")
    print(f"  CV Score:  {cross_val_scores[name].mean():.1%}")


# PHASE 6: FIND BEST MODEL


print("\n[PHASE 6] BEST MODEL SELECTION")
print("-" * 80)

best_model_name = max(results, key=lambda x: results[x]['f1'])
best_model = trained_models[best_model_name]
best_results = results[best_model_name]

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   F1-Score: {best_results['f1']:.1%}")
print(f"   Accuracy: {best_results['accuracy']:.1%}")
print(f"   Precision: {best_results['precision']:.1%}")
print(f"   Recall: {best_results['recall']:.1%}")

# PHASE 7: DETAILED ANALYSIS OF BEST MODEL


print("\n[PHASE 7] DETAILED ANALYSIS")
print("-" * 80)

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, best_results['y_pred'])
print(f"  True Negatives:  {cm[0][0]}")
print(f"  False Positives: {cm[0][1]}")
print(f"  False Negatives: {cm[1][0]}")
print(f"  True Positives:  {cm[1][1]}")

print("\nDetailed Classification Report:")
print(classification_report(y_test, best_results['y_pred'], 
                          target_names=['Legitimate', 'Spam']))


# PHASE 8: FEATURE IMPORTANCE (for tree-based models)


print("\n[PHASE 8] FEATURE IMPORTANCE ANALYSIS")
print("-" * 80)

if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    indices = np.argsort(importances)[-10:]
    
    print("Top 10 important features:")
    for idx, i in enumerate(reversed(indices)):
        print(f"  {idx+1}. {feature_names[i]}: {importances[i]:.4f}")
elif best_model_name == 'Naive Bayes':
    print("Naive Bayes uses probabilistic features.")
    print("Most discriminative terms are those with highest frequency difference.")
else:
    print("Feature importance not available for this model type.")


# PHASE 9: REAL-WORLD PREDICTIONS


print("\n[PHASE 9] REAL-WORLD PREDICTIONS")
print("-" * 80)

def predict_email(email_text):
    cleaned = preprocess_text(email_text)
    features = tfidf.transform([cleaned])
    
    pred = best_model.predict(features)[0]
    try:
        prob = best_model.predict_proba(features)[0]
        confidence = max(prob) * 100
    except:
        confidence = None
    
    return pred, confidence

test_emails = [
    "Click here to claim your free prize now!!!",
    "Let's schedule a meeting for next week",
    "URGENT: Verify your banking details immediately",
    "The project report is attached for review",
    "You have won a luxury vacation package",
    "Can we discuss the budget for Q4?",
]

print("\nPredicting on new emails:\n")
for email in test_emails:
    pred, conf = predict_email(email)
    label = "🚨 SPAM" if pred == 1 else "✓ LEGITIMATE"
    conf_str = f" (Confidence: {conf:.1f}%)" if conf else ""
    print(f"Email: \"{email}\"")
    print(f"Result: {label}{conf_str}\n")


# PHASE 10: MODEL PERSISTENCE


print("\n[PHASE 10] MODEL PERSISTENCE")
print("-" * 80)

# Save best model
model_filename = 'spam_classifier_model.pkl'
vectorizer_filename = 'tfidf_vectorizer.pkl'

with open(model_filename, 'wb') as f:
    pickle.dump(best_model, f)

with open(vectorizer_filename, 'wb') as f:
    pickle.dump(tfidf, f)

print(f"✓ Model saved to: {model_filename}")
print(f"✓ Vectorizer saved to: {vectorizer_filename}")

# Save metadata
metadata = {
    'model_type': best_model_name,
    'accuracy': float(best_results['accuracy']),
    'precision': float(best_results['precision']),
    'recall': float(best_results['recall']),
    'f1_score': float(best_results['f1']),
    'training_date': datetime.now().isoformat(),
    'total_features': X.shape[1],
    'training_samples': X_train.shape[0]
}

with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✓ Metadata saved to: model_metadata.json")


# PHASE 11: PRODUCTION FLASK API (CODE ONLY, REQUIRES FLASK INSTALLATION)


print("\n[PHASE 11] FLASK API CODE GENERATED")
print("-" * 80)

api_code = '''
# Save this as app.py and run: python app.py
# Then visit: http://localhost:5000/api/predict

from flask import Flask, request, jsonify
import pickle
import json

app = Flask(__name__)

# Load models
with open('spam_classifier_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model_metadata.json', 'r') as f:
    metadata = json.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict if email is spam or not"""
    try:
        data = request.json
        email = data.get('email', '')
        
        if not email:
            return jsonify({'error': 'Email text required'}), 400
        
        # Preprocess
        email_cleaned = email.lower().strip()
        
        # Vectorize
        features = vectorizer.transform([email_cleaned])
        
        # Predict
        prediction = model.predict(features)[0]
        try:
            probabilities = model.predict_proba(features)[0]
            confidence = float(max(probabilities) * 100)
        except:
            confidence = None
        
        result = {
            'email': email,
            'prediction': 'SPAM' if prediction == 1 else 'LEGITIMATE',
            'is_spam': bool(prediction),
            'confidence': confidence,
            'model': metadata['model_type'],
            'accuracy': metadata['accuracy']
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify(metadata)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

print("Flask API code available. Features:")
print("  ✓ POST /api/predict - Classify emails")
print("  ✓ GET /api/model-info - Get model metadata")
print("  ✓ JSON request/response format")
print("  ✓ Error handling")
print("  ✓ Confidence scores")


# PHASE 12: SUMMARY & DEPLOYMENT READINESS


print("\n[PHASE 12] PRODUCTION DEPLOYMENT SUMMARY")
print("=" * 80)

print("\n📊 MODEL PERFORMANCE COMPARISON:")
print("-" * 80)
for name, res in results.items():
    print(f"{name:20} F1: {res['f1']:.1%}  Accuracy: {res['accuracy']:.1%}")

print("\n🏆 SELECTED MODEL FOR PRODUCTION:")
print(f"  Model: {best_model_name}")
print(f"  Accuracy: {best_results['accuracy']:.1%}")
print(f"  Precision: {best_results['precision']:.1%}")
print(f"  Recall: {best_results['recall']:.1%}")
print(f"  F1-Score: {best_results['f1']:.1%}")

print("\n📁 GENERATED FILES:")
print(f"  ✓ spam_classifier_model.pkl - Trained model")
print(f"  ✓ tfidf_vectorizer.pkl - Text vectorizer")
print(f"  ✓ model_metadata.json - Model information")

print("\n🚀 DEPLOYMENT OPTIONS:")
print("  1. Flask REST API (local/cloud)")
print("  2. AWS Lambda function")
print("  3. Docker containerization")
print("  4. Streamlit web app")
print("  5. Real-time prediction service")

print("\n💡 NEXT IMPROVEMENTS:")
print("  1. Hyperparameter tuning with GridSearchCV")
print("  2. Add more advanced NLP (BERT, Word2Vec)")
print("  3. Implement ensemble methods")
print("  4. Add real-time monitoring/metrics")
print("  5. Performance optimization for large datasets")

print("\n" + "=" * 80)
print("PRODUCTION-READY EMAIL SPAM CLASSIFIER - COMPLETE!")
print("=" * 80)
