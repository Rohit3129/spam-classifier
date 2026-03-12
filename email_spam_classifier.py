


# STAGE 1: IMPORTS & SETUP


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("EMAIL SPAM CLASSIFIER - END-TO-END PIPELINE")
print("=" * 80)


# STAGE 2: DATA COLLECTION


print("\n[STAGE 1] DATA COLLECTION")

# Load real dataset from spam.csv
df = pd.read_csv('spam.csv', encoding='latin-1', usecols=[0,1])

# Rename columns
df.columns = ['label', 'email']

# Convert labels to numeric
df['label'] = (df['label'] == 'spam').astype(int)

print(f"✓ Loaded {len(df)} emails")
print(f"✓ Spam emails: {(df['label'] == 1).sum()}")
print(f"✓ Legitimate emails: {(df['label'] == 0).sum()}")

print("\nSample data:")
print(df.head())



# STAGE 3: DATA PREPROCESSING (NLP PART)


print("\n\n[STAGE 2] DATA PREPROCESSING & NLP")


def preprocess_text(text):
    """
    Preprocess email text:
    - Convert to lowercase
    - Remove extra whitespace
    - Remove special characters (keep simple)
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

# Apply preprocessing
df['email_cleaned'] = df['email'].apply(preprocess_text)

print(" Text preprocessing completed")
print("\nOriginal vs Cleaned:")
for i in range(2):
    print(f"\nOriginal: {df['email'].iloc[i]}")
    print(f"Cleaned:  {df['email_cleaned'].iloc[i]}")


# STAGE 4: FEATURE ENGINEERING


print("\n\n[STAGE 3] FEATURE ENGINEERING")




# Create TF-IDF vectors
tfidf = TfidfVectorizer(
    max_features=50,        # Use top 50 words
    stop_words='english',   # Remove common words (the, is, a)
    lowercase=True,
    min_df=1                # Word must appear in at least 1 document
)

# Fit and transform
X = tfidf.fit_transform(df['email_cleaned'])
y = df['label']

print(f" Feature extraction completed")
print(f" Feature matrix shape: {X.shape} (emails × features)")
print(f" Top 20 features (important words):")
feature_names = tfidf.get_feature_names_out()
for i, name in enumerate(feature_names[:20]):
    print(f"   {i+1}. {name}")


# STAGE 5: SPLIT DATA INTO TRAIN & TEST


print("\n\n[STAGE 4] TRAIN-TEST SPLIT")


X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.3,          # 30% for testing
    random_state=42,
    stratify=y              # Keep class distribution
)

print(f" Training set: {X_train.shape[0]} emails")
print(f" Testing set: {X_test.shape[0]} emails")
print(f" Train/Test split: 70% / 30%")


# STAGE 6: MODEL TRAINING (ML PART)


print("\n\n[STAGE 5] MODEL TRAINING")


"""
Naive Bayes Classifier:
- Simple but effective for text classification
- Uses probability to make predictions
- Fast to train and predict
"""

# Create and train model
model = MultinomialNB()
model.fit(X_train, y_train)

print("Model trained successfully")
print(f"Algorithm: Multinomial Naive Bayes")
print(f"Classes: 0 (Legitimate), 1 (Spam)")


# STAGE 7: MODEL EVALUATION


print("\n\n[STAGE 6] MODEL EVALUATION")


# Make predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)
precision = precision_score(y_test, y_pred_test)
recall = recall_score(y_test, y_pred_test)
f1 = f1_score(y_test, y_pred_test)

print("PERFORMANCE METRICS:")
print(f"  Training Accuracy: {train_accuracy:.2%}")
print(f"  Testing Accuracy:  {test_accuracy:.2%}")
print(f"  Precision:         {precision:.2%}  ")
print(f"  Recall:            {recall:.2%}  ")
print(f"  F1-Score:          {f1:.2%}  ")

print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred_test, 
                          target_names=['Legitimate', 'Spam']))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_test)
print(f"  True Negatives:  {cm[0][0]}  (Legit correctly identified)")
print(f"  False Positives: {cm[0][1]}  (Legit marked as spam)")
print(f"  False Negatives: {cm[1][0]}  (Spam marked as legit)")
print(f"  True Positives:  {cm[1][1]}  (Spam correctly identified)")


# STAGE 8: MAKE PREDICTIONS ON NEW DATA


print("\n\n[STAGE 7] REAL-WORLD PREDICTIONS")


def predict_email(email_text):
    """
    Complete pipeline in one function:
    1. Preprocess text
    2. Convert to features
    3. Make prediction
    """
    # Preprocess
    cleaned = preprocess_text(email_text)
    
    # Vectorize
    features = tfidf.transform([cleaned])
    
    # Predict
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    return prediction, probability

# Test on new emails
test_emails = [
    "Congratulations! You won a free vacation! Click now!",
    "Meeting rescheduled to 4pm tomorrow",
    "URGENT: Verify your account immediately or lose access",
    "The project documentation is ready for review"
]

print("Making predictions on new emails:\n")
for email in test_emails:
    pred, prob = predict_email(email)
    label = "SPAM " if pred == 1 else "LEGITIMATE "
    confidence = max(prob) * 100
    print(f"Email: \"{email}\"")
    print(f"  → Prediction: {label}")
    print(f"  → Confidence: {confidence:.1f}%")
    print()

# ============================================================================
# SUMMARY & INSIGHTS
# ============================================================================

print("\n" + "=" * 80)
print("PIPELINE SUMMARY")
print("=" * 80)

print("""
END-TO-END PIPELINE STAGES:

1. DATA COLLECTION
    Gathered 20 email examples (spam + legitimate)

2. DATA PREPROCESSING (NLP)
    Cleaned text: lowercase, whitespace removal

3. FEATURE ENGINEERING
    Converted text to numerical features using TF-IDF
    Created feature matrix (20 emails × 50 features)

4. TRAIN-TEST SPLIT
    70% training (14 emails), 30% testing (6 emails)

5. MODEL TRAINING (ML)
    Trained Naive Bayes classifier
    Model learned patterns between spam and legitimate

6. MODEL EVALUATION
    Tested accuracy: {:.0%}
    Verified performance with multiple metrics

7. DEPLOYMENT
    Making predictions on new, unseen emails
    Providing confidence scores"

""".format(test_accuracy))

print("PROJECT COMPLETE!")

