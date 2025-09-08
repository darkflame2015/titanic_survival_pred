"""
Titanic Survival Prediction Model Training Script
This script creates and trains a Random Forest classifier to predict Titanic passenger survival.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

class TitanicSurvivalPredictor:
    """
    A class to train and save a Titanic survival prediction model using Random Forest.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        self.label_encoders = {}
        self.feature_columns = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
        
    def create_sample_data(self):
        """
        Creates a synthetic dataset based on Titanic passenger characteristics.
        This is used since we don't have the actual Titanic dataset.
        """
        np.random.seed(42)
        
        # Generate sample data with realistic distributions
        num_samples = 1000
        
        data = {
            'pclass': np.random.choice([1, 2, 3], num_samples, p=[0.2, 0.2, 0.6]),
            'sex': np.random.choice(['male', 'female'], num_samples, p=[0.65, 0.35]),
            'age': np.random.normal(30, 12, num_samples).clip(1, 80),
            'sibsp': np.random.choice([0, 1, 2, 3, 4], num_samples, p=[0.7, 0.15, 0.1, 0.03, 0.02]),
            'parch': np.random.choice([0, 1, 2, 3], num_samples, p=[0.8, 0.12, 0.06, 0.02]),
            'fare': np.random.lognormal(3, 1, num_samples).clip(5, 500),
            'embarked': np.random.choice(['C', 'Q', 'S'], num_samples, p=[0.2, 0.1, 0.7])
        }
        
        df = pd.DataFrame(data)
        
        # Create survival target based on realistic patterns
        survival_prob = (
            (df['sex'] == 'female') * 0.4 +  # Women had higher survival rate
            (df['pclass'] == 1) * 0.3 +       # First class had higher survival rate
            (df['pclass'] == 2) * 0.15 +      # Second class moderate survival rate
            (df['age'] < 16) * 0.2 +          # Children had higher survival rate
            (df['fare'] > df['fare'].quantile(0.75)) * 0.1 +  # Higher fare = higher survival
            np.random.normal(0, 0.1, num_samples)  # Add some randomness
        ).clip(0, 1)
        
        df['survived'] = (np.random.random(num_samples) < survival_prob).astype(int)
        
        return df
    
    def preprocess_data(self, df):
        """
        Preprocesses the data for training/prediction.
        
        Args:
            df (pandas.DataFrame): Input dataframe
            
        Returns:
            pandas.DataFrame: Preprocessed dataframe
        """
        df = df.copy()
        
        # Handle missing values
        df['age'].fillna(df['age'].median(), inplace=True)
        df['fare'].fillna(df['fare'].median(), inplace=True)
        df['embarked'].fillna(df['embarked'].mode()[0], inplace=True)
        
        # Encode categorical variables
        categorical_columns = ['sex', 'embarked']
        
        for column in categorical_columns:
            if column not in self.label_encoders:
                self.label_encoders[column] = LabelEncoder()
                df[column] = self.label_encoders[column].fit_transform(df[column])
            else:
                # For prediction, use existing encoders
                df[column] = self.label_encoders[column].transform(df[column])
        
        return df
    
    def train_model(self):
        """
        Trains the Random Forest model and saves it along with the encoders.
        """
        print("Creating sample Titanic dataset...")
        df = self.create_sample_data()
        
        print("Preprocessing data...")
        df_processed = self.preprocess_data(df)
        
        # Prepare features and target
        X = df_processed[self.feature_columns]
        y = df_processed['survived']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Save the model and encoders
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """
        Saves the trained model and label encoders to disk.
        """
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the model
        joblib.dump(self.model, 'models/titanic_model.pkl')
        
        # Save the label encoders
        joblib.dump(self.label_encoders, 'models/label_encoders.pkl')
        
        # Save feature columns for reference
        joblib.dump(self.feature_columns, 'models/feature_columns.pkl')
        
        print("Model and encoders saved successfully!")
    
    def predict_survival(self, passenger_data):
        """
        Predicts survival probability for a single passenger.
        
        Args:
            passenger_data (dict): Dictionary containing passenger information
            
        Returns:
            tuple: (survival_probability, prediction)
        """
        # Create DataFrame from input
        df = pd.DataFrame([passenger_data])
        
        # Preprocess the data
        df_processed = self.preprocess_data(df)
        
        # Make prediction
        prediction = self.model.predict(df_processed[self.feature_columns])[0]
        probability = self.model.predict_proba(df_processed[self.feature_columns])[0][1]
        
        return probability, prediction

def main():
    """
    Main function to train and save the model.
    """
    print("=== Titanic Survival Prediction Model Training ===")
    
    predictor = TitanicSurvivalPredictor()
    accuracy = predictor.train_model()
    
    print(f"\n=== Training Complete! ===")
    print(f"Final Model Accuracy: {accuracy:.4f}")
    print("Model files saved in 'models/' directory")

if __name__ == "__main__":
    main()
