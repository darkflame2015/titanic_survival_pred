# Netlify Deployment Guide

This guide explains how to deploy the Titanic Survival Predictor to Netlify.

## Two Deployment Options

### Option 1: Simple Static Deployment (Recommended for Netlify)

Use the `netlify-version.html` file which contains a client-side prediction algorithm.

#### Steps:
1. **Prepare Files**:
   - Rename `netlify-version.html` to `index.html`
   - This file is self-contained with embedded CSS and JavaScript

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://www.netlify.com)
   - Drag and drop the `index.html` file to Netlify
   - Your site will be live instantly!

3. **Custom Domain** (Optional):
   - In Netlify dashboard, go to Site Settings → Domain management
   - Add your custom domain

#### Pros:
- ✅ No server required
- ✅ Instant deployment
- ✅ Free hosting
- ✅ Fast loading
- ✅ Works offline

#### Cons:
- ❌ Uses rule-based prediction (not ML model)
- ❌ Less accurate than trained model

### Option 2: Full-Stack Deployment

Deploy both frontend and backend using Netlify Functions or external API.

#### For Netlify Functions:

1. **Create `netlify.toml`**:
```toml
[build]
  functions = "functions"

[functions]
  python_runtime = "3.8"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

2. **Create Functions Directory**:
```
mkdir functions
```

3. **Create Function** (`functions/predict.py`):
```python
import json
import joblib
import pandas as pd

def handler(event, context):
    try:
        # Load model (you'll need to include model files)
        model = joblib.load('models/titanic_model.pkl')
        
        # Process request
        data = json.loads(event['body'])
        
        # Make prediction
        # ... (prediction logic)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

4. **Update JavaScript**:
   - Change API URL to `/.netlify/functions/predict`

#### Pros:
- ✅ Uses actual ML model
- ✅ More accurate predictions
- ✅ Serverless backend

#### Cons:
- ❌ More complex setup
- ❌ Requires Netlify Pro plan for Python functions
- ❌ Cold start delays

## Recommended Approach

For most users, **Option 1 (Static Deployment)** is recommended because:

1. **Simplicity**: Just upload one HTML file
2. **Cost**: Completely free
3. **Performance**: Fast loading, no server delays
4. **Reliability**: No server to crash or maintain

The rule-based prediction algorithm in the static version captures the main patterns:
- Women had higher survival rates
- First-class passengers survived more
- Children had better chances
- Family size affected survival

While not as accurate as the ML model, it demonstrates the concept effectively.

## File Structure for Netlify

### Option 1 (Static):
```
└── index.html (renamed from netlify-version.html)
```

### Option 2 (Full-Stack):
```
├── index.html
├── styles.css
├── script.js
├── netlify.toml
├── functions/
│   └── predict.py
└── models/
    ├── titanic_model.pkl
    ├── label_encoders.pkl
    └── feature_columns.pkl
```

## Testing Locally

Before deploying, test the static version:

1. **Open File**: Double-click `netlify-version.html`
2. **Test Form**: Fill in passenger details
3. **Check Results**: Verify predictions appear correctly
4. **Responsive**: Test on mobile devices

## Post-Deployment

After deployment:

1. **Test Live Site**: Try different passenger combinations
2. **Check Performance**: Verify fast loading
3. **Mobile Testing**: Test on various devices
4. **Share**: Get feedback from users

## Custom Improvements

You can enhance the static version:

1. **Better Algorithm**: Improve the rule-based prediction
2. **More Features**: Add passenger name, ticket number fields
3. **Animations**: Add loading animations and transitions
4. **Historical Data**: Include real Titanic facts
5. **Multiple Models**: Compare different prediction approaches

## Conclusion

The static deployment option provides an excellent demonstration of the Titanic survival prediction concept while being easy to deploy and maintain on Netlify.
