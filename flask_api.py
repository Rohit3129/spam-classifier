"""
================================================================================
FLASK REST API FOR SPAM CLASSIFIER
================================================================================

This is a PRODUCTION-READY API for the spam classifier.

Installation:
    pip install flask

Running:
    python flask_api.py

Testing:
    curl -X POST http://localhost:5000/api/predict \
      -H "Content-Type: application/json" \
      -d '{"email": "Click here to win money!!!"}'

================================================================================
"""

from flask import Flask, request, jsonify
import pickle
import json
import os
from datetime import datetime
import logging

# ============================================================================
# SETUP
# ============================================================================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# LOAD MODELS & METADATA
# ============================================================================

def load_models():
    """Load trained model and vectorizer"""
    try:
        # First, check if models exist
        if not os.path.exists('spam_classifier_model.pkl'):
            logger.warning("Model file not found. Run advanced_spam_classifier.py first!")
            return None, None, None
        
        with open('spam_classifier_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        
        with open('model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        logger.info("✓ Models loaded successfully")
        return model, vectorizer, metadata
    
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return None, None, None

# Load models at startup
MODEL, VECTORIZER, METADATA = load_models()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def preprocess_text(text):
    """Clean and preprocess email text"""
    text = text.lower()
    text = ' '.join(text.split())
    return text

def get_prediction(email_text):
    """Make prediction on email"""
    if MODEL is None or VECTORIZER is None:
        raise Exception("Model not loaded. Run advanced_spam_classifier.py first!")
    
    # Preprocess
    cleaned = preprocess_text(email_text)
    
    # Vectorize
    features = VECTORIZER.transform([cleaned])
    
    # Predict
    prediction = MODEL.predict(features)[0]
    
    # Get confidence
    try:
        probabilities = MODEL.predict_proba(features)[0]
        confidence = float(max(probabilities) * 100)
    except AttributeError:
        # For models that don't have predict_proba (like SVM)
        confidence = None
    
    return {
        'is_spam': bool(prediction),
        'prediction': 'SPAM' if prediction == 1 else 'LEGITIMATE',
        'confidence': confidence
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    status = "healthy" if MODEL is not None else "unhealthy"
    return jsonify({
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'model_loaded': MODEL is not None
    })

# ============================================================================
# PREDICTION ENDPOINT
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict if email is spam or legitimate
    
    Request:
        {
            "email": "Email text to classify"
        }
    
    Response:
        {
            "email": "Input email",
            "prediction": "SPAM" or "LEGITIMATE",
            "is_spam": true/false,
            "confidence": 95.5,
            "model": "SVM",
            "timestamp": "2025-03-12T..."
        }
    """
    try:
        # Validate request
        if not request.json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        email = request.json.get('email', '').strip()
        
        if not email:
            return jsonify({'error': 'Email text is required'}), 400
        
        if len(email) > 5000:
            return jsonify({'error': 'Email text too long (max 5000 chars)'}), 400
        
        # Make prediction
        result = get_prediction(email)
        
        # Build response
        response = {
            'success': True,
            'email': email[:100] + '...' if len(email) > 100 else email,
            'prediction': result['prediction'],
            'is_spam': result['is_spam'],
            'confidence': result['confidence'],
            'model': METADATA['model_type'] if METADATA else 'Unknown',
            'model_accuracy': METADATA['accuracy'] if METADATA else None,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# BATCH PREDICTION ENDPOINT
# ============================================================================

@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Classify multiple emails at once
    
    Request:
        {
            "emails": [
                "Email 1",
                "Email 2",
                ...
            ]
        }
    
    Response:
        {
            "predictions": [
                {
                    "email": "...",
                    "prediction": "SPAM",
                    "confidence": 95.5
                },
                ...
            ]
        }
    """
    try:
        if not request.json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        emails = request.json.get('emails', [])
        
        if not emails:
            return jsonify({'error': 'Emails list is required'}), 400
        
        if not isinstance(emails, list):
            return jsonify({'error': 'Emails must be a list'}), 400
        
        if len(emails) > 100:
            return jsonify({'error': 'Maximum 100 emails per request'}), 400
        
        # Make predictions
        predictions = []
        for email in emails:
            if isinstance(email, str) and email.strip():
                result = get_prediction(email)
                predictions.append({
                    'email': email[:100] + '...' if len(email) > 100 else email,
                    'prediction': result['prediction'],
                    'is_spam': result['is_spam'],
                    'confidence': result['confidence']
                })
        
        response = {
            'success': True,
            'count': len(predictions),
            'predictions': predictions,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# MODEL INFO ENDPOINT
# ============================================================================

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information and metadata"""
    if METADATA is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    return jsonify({
        'success': True,
        'model_type': METADATA.get('model_type'),
        'performance': {
            'accuracy': METADATA.get('accuracy'),
            'precision': METADATA.get('precision'),
            'recall': METADATA.get('recall'),
            'f1_score': METADATA.get('f1_score')
        },
        'training_info': {
            'training_date': METADATA.get('training_date'),
            'total_features': METADATA.get('total_features'),
            'training_samples': METADATA.get('training_samples')
        }
    }), 200

# ============================================================================
# STATS ENDPOINT
# ============================================================================

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get API usage statistics"""
    return jsonify({
        'success': True,
        'api_version': '1.0',
        'endpoints': {
            'POST /api/predict': 'Classify single email',
            'POST /api/predict-batch': 'Classify multiple emails',
            'GET /api/model-info': 'Get model information',
            'GET /health': 'Health check'
        },
        'model_loaded': MODEL is not None,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'POST /api/predict',
            'POST /api/predict-batch',
            'GET /api/model-info',
            'GET /health',
            'GET /api/stats'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    if MODEL is None:
        print("\n⚠️  WARNING: Models not found!")
        print("Please run: python advanced_spam_classifier.py")
        print("This will generate the required model files.\n")
    else:
        print("\n" + "="*80)
        print("FLASK API RUNNING")
        print("="*80)
        print("\n✓ Model loaded: {}".format(METADATA['model_type']))
        print("✓ Accuracy: {:.1%}".format(METADATA['accuracy']))
        print("\nAPI Endpoints:")
        print("  POST /api/predict           - Classify single email")
        print("  POST /api/predict-batch     - Classify multiple emails")
        print("  GET /api/model-info        - Get model information")
        print("  GET /health                - Health check")
        print("  GET /api/stats             - API statistics")
        print("\nTesting with curl:")
        print("  curl -X POST http://localhost:5000/api/predict \\")
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"email": "Click here to win money!!!"}\'\n')
        print("="*80 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
