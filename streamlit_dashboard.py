"""
================================================================================
STREAMLIT WEB DASHBOARD FOR SPAM CLASSIFIER
================================================================================

This is a beautiful web interface for your spam classifier.

Installation:
    pip install streamlit

Running:
    streamlit run streamlit_dashboard.py

Then open: http://localhost:8501

================================================================================
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Email Spam Classifier",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #ff4b4b;
    color: white;
}

div[data-testid="stMetric"] label {
    color: #cbd5e1 !important;
}

div[data-testid="stMetric"] div {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODELS
# ============================================================================

@st.cache_resource
def load_model():
    """Load trained model and vectorizer"""
    try:
        # Try to load from advanced version
        if os.path.exists('spam_classifier_model.pkl'):
            with open('spam_classifier_model.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('tfidf_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            with open('model_metadata.json', 'r') as f:
                import json
                metadata = json.load(f)
            return model, vectorizer, metadata
    except:
        pass
    
    st.error("Models not found! Please run advanced_spam_classifier.py first.")
    return None, None, None

model, vectorizer, metadata = load_model()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def preprocess_text(text):
    """Clean and preprocess email text"""
    text = text.lower()
    text = ' '.join(text.split())
    return text

def predict_email(email_text):
    """Make prediction on email"""
    if model is None:
        return None, None
    
    # Preprocess
    cleaned = preprocess_text(email_text)
    
    # Vectorize
    features = vectorizer.transform([cleaned])
    
    # Predict
    prediction = model.predict(features)[0]
    
    # Get confidence
    try:
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities) * 100)
    except:
        confidence = None
    
    return prediction, confidence

# ============================================================================
# MAIN APP
# ============================================================================

# Header
st.title(" Email Spam Classifier")
st.write("Intelligent email classification using Machine Learning")

# Check if model is loaded
if model is None:
    st.error(" Models not loaded. Please run: `python advanced_spam_classifier.py`")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("🔧 Settings")
page = st.sidebar.radio(
    "Choose a page:",
    [" Home", " Single Email", " Batch Upload", " Statistics", "ℹ About"]
)

# Model info in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader(" Model Information")
if metadata:
    st.sidebar.metric("Accuracy", f"{metadata['accuracy']:.1%}")
    st.sidebar.metric("Precision", f"{metadata['precision']:.1%}")
    st.sidebar.metric("F1-Score", f"{metadata['f1_score']:.1%}")
    st.sidebar.metric("Model Type", metadata['model_type'])

# ============================================================================
# PAGE 1: HOME
# ============================================================================

if page == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Welcome! 👋")
        st.write("""
        This app classifies emails as **SPAM** or **LEGITIMATE** using 
        advanced machine learning algorithms.
        
        ### Features:
        -  Single email classification
        -  Batch upload (CSV files)
        -  Performance statistics
        -  Real-time predictions
        
        ### Get Started:
        1. Click ** Single Email** to classify one email
        2. Or click ** Batch Upload** to classify many emails
        3. View ** Statistics** for model performance
        """)
    
    with col2:
        st.subheader("How it works ")
        st.markdown("""
        ```
        Email Text
            ↓
        Text Preprocessing (Clean)
            ↓
        Feature Extraction (TF-IDF)
            ↓
        ML Model Prediction
            ↓
        SPAM or LEGITIMATE
        ```
        """)
    
    # Quick stats
    st.markdown("---")
    st.subheader("Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", f"{metadata['accuracy']:.1%}" if metadata else "N/A")
    with col2:
        st.metric("Precision", f"{metadata['precision']:.1%}" if metadata else "N/A")
    with col3:
        st.metric("Recall", f"{metadata['recall']:.1%}" if metadata else "N/A")
    with col4:
        st.metric("F1-Score", f"{metadata['f1_score']:.1%}" if metadata else "N/A")

# ============================================================================
# PAGE 2: SINGLE EMAIL PREDICTION
# ============================================================================

elif page == " Single Email":
    st.subheader("Classify a Single Email")
    
    # Email input
    col1, col2 = st.columns([3, 1])
    with col1:
        email_input = st.text_area(
            "Enter email content below:",
            height=200,
            placeholder="Type or paste the email text here..."
        )
    
    with col2:
        st.write("")  # Spacing
        classify_button = st.button(
            " Classify Email",
            use_container_width=True,
            help="Click to classify the email"
        )
    
    # Process and display result
    if classify_button:
        if email_input.strip():

            with st.spinner("Analyzing email..."):
                prediction, confidence = predict_email(email_input)

            #  FIX FOR NONE CONFIDENCE
            confidence_display = f"{confidence:.1f}%" if confidence is not None else "N/A"

            st.markdown("---")

            if prediction == 1:

                st.markdown(
                    f"""
                    <div class="danger-box">
                    <h3> This is SPAM</h3>
                    <p>Confidence: <strong>{confidence_display}</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.warning(" We recommend not responding to this email")

            else:

                st.markdown(
                    f"""
                    <div class="success-box">
                    <h3> This is LEGITIMATE</h3>
                    <p>Confidence: <strong>{confidence_display}</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.success(" This email appears to be genuine")

            with st.expander("Email Preview"):
                st.write(email_input)

        else:
            st.warning("Please enter email text")

# ============================================================================
# PAGE 3: BATCH UPLOAD
# ============================================================================

elif page == " Batch Upload":
    st.subheader("Classify Multiple Emails")
    
    st.write("Upload a CSV file with an 'email' column to classify multiple emails at once.")
    
    uploaded_file = st.file_uploader(
        "Upload CSV file:",
        type=['csv'],
        help="CSV must have an 'email' column"
    )
    
    if uploaded_file:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Check if email column exists
            if 'email' not in df.columns:
                st.error(f" CSV must have 'email' column. Found columns: {list(df.columns)}")
            else:
                st.success(f" Loaded {len(df)} emails")
                
                # Show preview
                with st.expander(" Data Preview"):
                    st.dataframe(df.head())
                
                # Classify all emails
                if st.button(" Classify All Emails"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    predictions = []
                    confidences = []
                    
                    for idx, email in enumerate(df['email']):
                        pred, conf = predict_email(str(email))
                        
                        predictions.append("SPAM" if pred == 1 else "LEGITIMATE")
                        confidences.append(conf if conf else 0)
                        
                        # Update progress
                        progress = (idx + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Classified {idx + 1}/{len(df)} emails...")
                    
                    # Add results to dataframe
                    df['Prediction'] = predictions
                    df['Confidence'] = [f"{c:.1f}%" if c else "N/A" for c in confidences]
                    
                    st.markdown("---")
                    st.subheader("Results")
                    
                    # Show statistics
                    spam_count = predictions.count("SPAM")
                    legit_count = predictions.count("LEGITIMATE")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total", len(df))
                    with col2:
                        st.metric("Spam", spam_count)
                    with col3:
                        st.metric("Legitimate", legit_count)
                    
                    # Display results table
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label=" Download Results as CSV",
                        data=csv,
                        file_name=f"spam_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Download the predictions as CSV file"
                    )
        
        except Exception as e:
            st.error(f"Error reading file: {e}")

# ============================================================================
# PAGE 4: STATISTICS
# ============================================================================

elif page == " Statistics":
    st.subheader("Model Performance Statistics")
    
    if metadata:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Accuracy",
                f"{metadata['accuracy']:.1%}",
                help="Overall correct predictions"
            )
        
        with col2:
            st.metric(
                "Precision",
                f"{metadata['precision']:.1%}",
                help="Of predicted SPAM, how many correct"
            )
        
        with col3:
            st.metric(
                "Recall",
                f"{metadata['recall']:.1%}",
                help="Of actual SPAM, how many caught"
            )
        
        with col4:
            st.metric(
                "F1-Score",
                f"{metadata['f1_score']:.1%}",
                help="Balance between Precision & Recall"
            )
        
        # Additional info
        st.markdown("---")
        st.subheader("Training Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Model Type:** {metadata['model_type']}")
            st.write(f"**Total Features:** {metadata['total_features']}")
        
        with col2:
            st.write(f"**Training Samples:** {metadata['training_samples']}")
            st.write(f"**Training Date:** {metadata['training_date']}")
        
        # Metrics explanation
        st.markdown("---")
        st.subheader(" Metrics Explanation")
        
        with st.expander("What do these metrics mean?"):
            st.markdown("""
            - **Accuracy**: Out of all predictions, how many were correct
            - **Precision**: Of emails predicted as SPAM, how many actually are SPAM
            - **Recall**: Of emails that actually are SPAM, how many did we catch
            - **F1-Score**: Balance between Precision and Recall (best overall metric)
            
            Example:
            - If Precision = 80%: Of 100 emails marked SPAM, 80 really are SPAM
            - If Recall = 90%: Of 100 actual SPAM emails, we caught 90 of them
            - F1-Score combines both to give overall performance
            """)

# ============================================================================
# PAGE 5: ABOUT
# ============================================================================

elif page == "ℹ About":
    st.subheader("About This Application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ###  How It Works
        
        This application uses **Machine Learning** to classify emails as SPAM 
        or LEGITIMATE.
        
        **Process:**
        1. Email text is cleaned and preprocessed
        2. Text is converted to numerical features using TF-IDF
        3. Machine Learning model makes a prediction
        4. Confidence score shows how sure the model is
        
        ###  Model Details
        
        - **Algorithm**: SVM (Support Vector Machine)
        - **Features**: TF-IDF with n-grams
        - **Training Data**: 5,000+ real emails
        - **Accuracy**: 75%+ with 80% F1-Score
        """)
    
    with col2:
        st.markdown("""
        ###  Technology Stack
        
        - **Frontend**: Streamlit
        - **Backend**: Python, Scikit-learn
        - **ML Model**: SVM with TF-IDF
        - **Database**: SQLite (optional)
        
        ### ⚡ Features
        
        -  Single email classification
        -  Batch processing
        -  Real-time predictions
        -  Performance metrics
        -  CSV export
        
        ###  Support
        
        For issues or questions:
        - GitHub: [https://github.com/Rohit3129/spam-classifier.git]
        - Email: rohitlamkhade301@.com
        """)
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888;">
        <p>Built with LOVE :) using Streamlit & Machine Learning</p>
        <p>© 2025 Email Spam Classifier | All Rights Reserved</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 12px;">
    <p>Email Spam Classifier v1.0 | Powered by Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
