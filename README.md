# Titanic Survival Predictor

A machine learning web application that predicts passenger survival on the Titanic using a Random Forest classifier. Built with Python, scikit-learn, Flask, and vanilla JavaScript.

## Features

- **Machine Learning Model**: Random Forest classifier trained on synthetic Titanic data
- **Web Interface**: Clean, responsive UI for entering passenger details
- **Real-time Predictions**: Instant survival probability calculations
- **Visual Results**: Interactive probability bars and confidence scores
- **Netlify Ready**: Optimized for easy deployment

## Project Structure

```
titanic_survival_pred/
├── train_model.py      # ML model training script
├── app.py             # Flask API server
├── index.html         # Frontend HTML
├── styles.css         # CSS styling
├── script.js          # JavaScript functionality
├── requirements.txt   # Python dependencies
├── models/           # Trained model files (created after training)
│   ├── titanic_model.pkl
│   ├── label_encoders.pkl
│   └── feature_columns.pkl
└── README.md         # This file
```

## Setup Instructions

### 1. Train the Model

First, train the machine learning model:

```bash
python train_model.py
```

This will:
- Create synthetic Titanic dataset
- Train a Random Forest classifier
- Save the model and encoders to the `models/` directory
- Display training accuracy and feature importance

### 2. Start the API Server

Run the Flask API server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Open the Web Interface

Open `index.html` in your web browser, or serve it using a local server:

```bash
# Using Python's built-in server
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

## Usage

1. **Enter Passenger Details**:
   - Passenger Class (1st, 2nd, or 3rd)
   - Gender (Male/Female)
   - Age (0-100 years)
   - Number of siblings/spouses aboard
   - Number of parents/children aboard
   - Fare paid (in pounds)
   - Port of embarkation (Cherbourg, Queenstown, Southampton)

2. **Get Prediction**:
   - Click "Predict Survival"
   - View survival probability
   - See confidence score
   - Analyze probability breakdown

## API Endpoints

### GET `/`
Returns API information and available endpoints.

### GET `/health`
Health check endpoint to verify API status.

### POST `/predict`
Main prediction endpoint.

**Request Body**:
```json
{
    "pclass": 3,
    "sex": "male",
    "age": 22,
    "sibsp": 1,
    "parch": 0,
    "fare": 7.25,
    "embarked": "S"
}
```

**Response**:
```json
{
    "prediction": 0,
    "survival_probability": 0.23,
    "death_probability": 0.77,
    "prediction_text": "Did not survive",
    "confidence": 0.77
}
```

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 7 input features (pclass, sex, age, sibsp, parch, fare, embarked)
- **Training Data**: 1000 synthetic samples based on historical Titanic patterns
- **Accuracy**: ~85% (varies with random seed)

### Feature Importance (typical results):
1. Sex (gender) - highest importance
2. Fare - second highest
3. Age - moderate importance
4. Passenger class - moderate importance
5. Other features - lower importance

## Deployment

### For Netlify (Static Site):

1. **Build Static Version**: Create a version that uses a public API or includes the model in JavaScript
2. **Upload Files**: Upload HTML, CSS, and JS files to Netlify
3. **Configure Build**: Set up build commands if needed

### For Heroku (Full Stack):

1. Create `Procfile`:
```
web: python app.py
```

2. Add to `requirements.txt` if needed:
```
gunicorn==20.1.0
```

3. Deploy to Heroku with both frontend and backend

## Customization

### Modify the Model:
- Edit `train_model.py` to change algorithms or parameters
- Retrain with your own dataset
- Adjust feature engineering

### Update the UI:
- Modify `styles.css` for different styling
- Edit `index.html` for layout changes
- Update `script.js` for new functionality

### API Changes:
- Extend `app.py` with new endpoints
- Add validation or preprocessing
- Include additional features

## Dependencies

- **Python**: 3.8+
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning
- **flask**: Web API framework
- **flask-cors**: Cross-origin requests
- **joblib**: Model serialization

## Notes

- This uses synthetic data for demonstration purposes
- Real Titanic data would require different preprocessing
- Model accuracy can be improved with more sophisticated features
- The web interface is designed to be simple and educational

## License

This project is for educational purposes. Feel free to modify and use as needed.
