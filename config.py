# Configuration settings for the application
APP_CONFIG = {
    'min_age': 18,
    'max_age': 80,
    'min_bmi': 16.0,
    'max_bmi': 35.0,
    'risk_score_ranges': {
        'low': (0, 33),
        'moderate': (34, 66),
        'high': (67, 100)
    }
}

# Model configuration parameters
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'random_state': 42
    },
    'kmeans': {
        'n_clusters': 5,
        'random_state': 42
    }
}

# Feature columns used in the models
FEATURES = ['Age', 'BMI', 'HealthRiskScore']
