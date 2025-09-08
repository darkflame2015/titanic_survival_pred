"""
Flask API for Titanic Survival Prediction
This script creates a web API to serve the trained model for predictions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow frontend access

class TitanicPredictor:
    """
    A class to load the trained model and make predictions.
    """
    
    def __init__(self):
        self.model = None
        self.label_encoders = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """
        Loads the trained model and encoders from disk.
        """
        try:
            self.model = joblib.load('models/titanic_model.pkl')
            self.label_encoders = joblib.load('models/label_encoders.pkl')
            self.feature_columns = joblib.load('models/feature_columns.pkl')
            print("Model loaded successfully!")
        except FileNotFoundError:
            print("Model files not found. Please train the model first by running train_model.py")
            raise
    
    def preprocess_input(self, passenger_data):
        """
        Preprocesses input data for prediction.
        
        Args:
            passenger_data (dict): Raw passenger data from API
            
        Returns:
            pandas.DataFrame: Preprocessed data ready for prediction
        """
        # Create DataFrame
        df = pd.DataFrame([passenger_data])
        
        # Handle missing values
        df['age'].fillna(30, inplace=True)  # Default age
        df['fare'].fillna(32.2, inplace=True)  # Default fare (median)
        
        # Ensure embarked is not empty
        if pd.isna(df['embarked'].iloc[0]) or df['embarked'].iloc[0] == '':
            df['embarked'] = 'S'  # Default to Southampton
        
        # Encode categorical variables
        categorical_columns = ['sex', 'embarked']
        
        for column in categorical_columns:
            if column in self.label_encoders:
                try:
                    df[column] = self.label_encoders[column].transform(df[column])
                except ValueError:
                    # Handle unseen categories
                    if column == 'sex':
                        df[column] = 0  # Default to male
                    elif column == 'embarked':
                        df[column] = 2  # Default to Southampton
        
        return df
    
    def predict(self, passenger_data):
        """
        Makes a survival prediction for a passenger.
        
        Args:
            passenger_data (dict): Passenger information
            
        Returns:
            dict: Prediction results
        """
        try:
            # Preprocess the data
            df_processed = self.preprocess_input(passenger_data)
            
            # Make prediction
            prediction = self.model.predict(df_processed[self.feature_columns])[0]
            probability = self.model.predict_proba(df_processed[self.feature_columns])[0]
            
            survival_probability = probability[1]  # Probability of survival
            death_probability = probability[0]     # Probability of death
            
            return {
                'prediction': int(prediction),
                'survival_probability': float(survival_probability),
                'death_probability': float(death_probability),
                'prediction_text': 'Survived' if prediction == 1 else 'Did not survive',
                'confidence': float(max(survival_probability, death_probability))
            }
        
        except Exception as e:
            return {
                'error': f"Prediction failed: {str(e)}"
            }

# Initialize the predictor
predictor = TitanicPredictor()

@app.route('/')
def home():
    """
    Home endpoint with API information.
    """
    return jsonify({
        'message': 'Titanic Survival Prediction API',
        'version': '1.0',
        'endpoints': {
            'predict': '/predict (POST)',
            'health': '/health (GET)'
        }
    })

@app.route('/health')
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint.
    
    Expected JSON payload:
    {
        "pclass": 3,
        "sex": "male",
        "age": 22,
        "sibsp": 1,
        "parch": 0,
        "fare": 7.25,
        "embarked": "S"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Make prediction
        result = predictor.predict(data)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/predict_form', methods=['POST'])
def predict_form():
    """
    Prediction endpoint for form data (alternative to JSON).
    """
    try:
        # Get form data
        data = {
            'pclass': int(request.form.get('pclass', 3)),
            'sex': request.form.get('sex', 'male'),
            'age': float(request.form.get('age', 30)),
            'sibsp': int(request.form.get('sibsp', 0)),
            'parch': int(request.form.get('parch', 0)),
            'fare': float(request.form.get('fare', 32.2)),
            'embarked': request.form.get('embarked', 'S')
        }
        
        # Make prediction
        result = predictor.predict(data)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Form processing error: {str(e)}'}), 500

if __name__ == '__main__':
    # Check if model exists
    if not os.path.exists('models/titanic_model.pkl'):
        print("Model not found! Please run train_model.py first.")
        exit(1)
    
    print("Starting Titanic Survival Prediction API...")
    print("API will be available at http://localhost:5000")
    print("Use /predict endpoint for JSON predictions")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
