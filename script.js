/**
 * Titanic Survival Predictor JavaScript
 * Handles form submission and displays prediction results
 */

// Configuration
const CONFIG = {
    API_URL: 'http://localhost:5000',  // Flask API URL
    PREDICTION_ENDPOINT: '/predict'
};

// DOM Elements
const form = document.getElementById('prediction-form');
const resultsDiv = document.getElementById('results');
const errorDiv = document.getElementById('error');
const predictBtn = document.querySelector('.predict-btn');
const btnText = document.querySelector('.btn-text');
const loadingText = document.querySelector('.loading');

// Result elements
const predictionText = document.getElementById('prediction-text');
const confidence = document.getElementById('confidence');
const survivalBar = document.getElementById('survival-bar');
const deathBar = document.getElementById('death-bar');
const survivalPercent = document.getElementById('survival-percent');
const deathPercent = document.getElementById('death-percent');
const errorMessage = document.getElementById('error-message');

/**
 * Initializes the application
 */
function init() {
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation
    addInputValidation();
    
    console.log('Titanic Survival Predictor initialized');
}

/**
 * Handles form submission
 * @param {Event} e - Form submit event
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Hide previous results/errors
    hideResults();
    hideError();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Get form data
        const formData = getFormData();
        
        // Validate form data
        if (!validateFormData(formData)) {
            throw new Error('Please fill in all required fields with valid values');
        }
        
        // Make prediction
        const result = await makePrediction(formData);
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Prediction error:', error);
        displayError(error.message);
    } finally {
        setLoadingState(false);
    }
}

/**
 * Gets form data as an object
 * @returns {Object} Form data
 */
function getFormData() {
    const formData = new FormData(form);
    
    return {
        pclass: parseInt(formData.get('pclass')),
        sex: formData.get('sex'),
        age: parseFloat(formData.get('age')),
        sibsp: parseInt(formData.get('sibsp')),
        parch: parseInt(formData.get('parch')),
        fare: parseFloat(formData.get('fare')),
        embarked: formData.get('embarked')
    };
}

/**
 * Validates form data
 * @param {Object} data - Form data to validate
 * @returns {boolean} Validation result
 */
function validateFormData(data) {
    // Check for required fields
    const requiredFields = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked'];
    
    for (let field of requiredFields) {
        if (data[field] === null || data[field] === undefined || data[field] === '') {
            return false;
        }
    }
    
    // Validate ranges
    if (data.pclass < 1 || data.pclass > 3) return false;
    if (data.age < 0 || data.age > 100) return false;
    if (data.sibsp < 0 || data.sibsp > 10) return false;
    if (data.parch < 0 || data.parch > 10) return false;
    if (data.fare < 0) return false;
    if (!['male', 'female'].includes(data.sex)) return false;
    if (!['C', 'Q', 'S'].includes(data.embarked)) return false;
    
    return true;
}

/**
 * Makes prediction API call
 * @param {Object} data - Passenger data
 * @returns {Promise<Object>} Prediction result
 */
async function makePrediction(data) {
    const response = await fetch(`${CONFIG.API_URL}${CONFIG.PREDICTION_ENDPOINT}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.error) {
        throw new Error(result.error);
    }
    
    return result;
}

/**
 * Displays prediction results
 * @param {Object} result - Prediction result from API
 */
function displayResults(result) {
    // Set prediction text and styling
    predictionText.textContent = result.prediction_text;
    predictionText.className = `outcome-text ${result.prediction === 1 ? 'survived' : 'not-survived'}`;
    
    // Set confidence
    confidence.textContent = `Confidence: ${(result.confidence * 100).toFixed(1)}%`;
    
    // Set probability bars and percentages
    const survivalPercentage = result.survival_probability * 100;
    const deathPercentage = result.death_probability * 100;
    
    survivalBar.style.width = `${survivalPercentage}%`;
    deathBar.style.width = `${deathPercentage}%`;
    
    survivalPercent.textContent = `${survivalPercentage.toFixed(1)}%`;
    deathPercent.textContent = `${deathPercentage.toFixed(1)}%`;
    
    // Show results
    showResults();
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Displays error message
 * @param {string} message - Error message to display
 */
function displayError(message) {
    errorMessage.textContent = message;
    showError();
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Sets loading state for the form
 * @param {boolean} isLoading - Whether to show loading state
 */
function setLoadingState(isLoading) {
    predictBtn.disabled = isLoading;
    
    if (isLoading) {
        btnText.style.display = 'none';
        loadingText.style.display = 'inline';
    } else {
        btnText.style.display = 'inline';
        loadingText.style.display = 'none';
    }
}

/**
 * Shows results section
 */
function showResults() {
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Hides results section
 */
function hideResults() {
    resultsDiv.style.display = 'none';
}

/**
 * Shows error section
 */
function showError() {
    errorDiv.style.display = 'block';
}

/**
 * Hides error section
 */
function hideError() {
    errorDiv.style.display = 'none';
}

/**
 * Adds input validation and user experience enhancements
 */
function addInputValidation() {
    // Age input validation
    const ageInput = document.getElementById('age');
    ageInput.addEventListener('input', function() {
        if (this.value < 0) this.value = 0;
        if (this.value > 100) this.value = 100;
    });
    
    // Fare input validation
    const fareInput = document.getElementById('fare');
    fareInput.addEventListener('input', function() {
        if (this.value < 0) this.value = 0;
    });
    
    // Siblings/Spouses validation
    const sibspInput = document.getElementById('sibsp');
    sibspInput.addEventListener('input', function() {
        if (this.value < 0) this.value = 0;
        if (this.value > 10) this.value = 10;
    });
    
    // Parents/Children validation
    const parchInput = document.getElementById('parch');
    parchInput.addEventListener('input', function() {
        if (this.value < 0) this.value = 0;
        if (this.value > 10) this.value = 10;
    });
}

/**
 * Utility function to format numbers
 * @param {number} num - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
function formatNumber(num, decimals = 1) {
    return Number(num).toFixed(decimals);
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

// Handle potential API connection issues
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    
    if (event.reason.message.includes('fetch')) {
        displayError('Unable to connect to the prediction service. Please make sure the API server is running.');
    }
});

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getFormData,
        validateFormData,
        makePrediction,
        displayResults,
        displayError
    };
}
