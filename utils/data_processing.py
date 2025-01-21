import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_data(df):
    """Preprocess the input data"""
    df = df.copy()
    df['BMI'] = df['BMI'].round(2)
    return df


def create_user_features(age, bmi):
    """Create feature vector for user"""
    return np.array([[age, bmi]])


def scale_features(features, scaler=None):
    """Scale features using StandardScaler"""
    if scaler is None:
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
    else:
        scaled_features = scaler.transform(features)
    return scaled_features, scaler


def find_similar_users(user_features, historical_data, n_neighbors=5):
    """Find similar users based on features"""
    # Ensure we're only using Age and BMI for comparison
    if historical_data.shape[1] > 2:
        historical_data = historical_data[:, :2]  # Take only first two columns (Age and BMI)

    similarities = cosine_similarity(user_features, historical_data)
    similar_indices = similarities[0].argsort()[-n_neighbors:][::-1]
    return similar_indices

def calculate_health_metrics(age, bmi, conditions):
    """Calculate basic health metrics"""
    base_score = 100 - (age * 0.3)  # Age factor
    bmi_factor = abs(25 - bmi) * 2  # BMI deviation from ideal
    condition_factor = len(conditions) * 10

    health_score = max(0, min(100, base_score - bmi_factor - condition_factor))
    return health_score