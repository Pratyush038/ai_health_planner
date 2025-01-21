from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import List, Tuple, Union
import pandas as pd


def find_similar_profiles(
        target_profile: dict,
        dataset: pd.DataFrame,
        n_matches: int = 5,
        features: List[str] = ['Age', 'BMI', 'HealthRiskScore']
) -> pd.DataFrame:
    """
    Find similar health profiles in the dataset based on user input.

    Parameters:
    target_profile (dict): Dictionary containing user's profile data
    dataset (pd.DataFrame): Reference dataset containing historical profiles
    n_matches (int): Number of similar profiles to return
    features (List[str]): Features to consider for similarity matching

    Returns:
    pd.DataFrame: DataFrame containing similar profiles
    """
    # Verify that all required features are present in the dataset
    if not all(feature in dataset.columns for feature in features):
        raise ValueError(f"Dataset missing required features. Required: {features}")

    # Ensure dataset is not empty
    if len(dataset) == 0:
        raise ValueError("Dataset is empty")

    # Ensure n_matches is not larger than dataset
    n_matches = min(n_matches, len(dataset))

    try:
        # Extract features from target profile
        target_values = np.array([[target_profile[feature] for feature in features]])

        # Extract features from dataset
        dataset_values = dataset[features].values

        # Handle NaN values if any
        if np.isnan(dataset_values).any() or np.isnan(target_values).any():
            raise ValueError("Input data contains NaN values")

        # Scale the features
        scaler = StandardScaler()
        dataset_scaled = scaler.fit_transform(dataset_values)
        target_scaled = scaler.transform(target_values)

        # Calculate Euclidean distances
        distances = np.sqrt(((dataset_scaled - target_scaled) ** 2).sum(axis=1))

        # Find indices of n most similar profiles
        similar_indices = distances.argsort()[:n_matches]

        # Calculate similarity scores (inverse of normalized distance)
        max_distance = distances.max() if distances.max() > 0 else 1
        similarity_scores = (1 - (distances[similar_indices] / max_distance)) * 100

        # Get similar profiles
        similar_profiles = dataset.iloc[similar_indices].copy()
        similar_profiles['SimilarityScore'] = similarity_scores.round(2)

        return similar_profiles.sort_values('SimilarityScore', ascending=False)

    except Exception as e:
        raise Exception(f"Error in finding similar profiles: {str(e)}")


def get_risk_category(risk_score: float) -> str:
    """
    Determine risk category based on health risk score.

    Parameters:
    risk_score (float): Health risk score

    Returns:
    str: Risk category
    """
    try:
        risk_score = float(risk_score)
        if risk_score < 30:
            return "Low"
        elif risk_score < 60:
            return "Moderate"
        else:
            return "High"
    except (ValueError, TypeError):
        return "Unknown"


def get_profile_insights(similar_profiles: pd.DataFrame) -> dict:
    """
    Generate insights based on similar profiles.

    Parameters:
    similar_profiles (pd.DataFrame): DataFrame of similar profiles

    Returns:
    dict: Dictionary containing insights
    """
    try:
        if len(similar_profiles) == 0:
            return {
                'avg_risk_score': 0,
                'risk_distribution': {},
                'common_diet': 'Unknown',
                'avg_exercise_capacity': 0,
                'age_range': {'min': 0, 'max': 0}
            }

        mode_diet = similar_profiles['DietaryPreference'].mode()
        common_diet = mode_diet.iloc[0] if not mode_diet.empty else 'Unknown'

        insights = {
            'avg_risk_score': similar_profiles['HealthRiskScore'].mean(),
            'risk_distribution': similar_profiles['HealthRiskScore'].apply(get_risk_category).value_counts().to_dict(),
            'common_diet': common_diet,
            'avg_exercise_capacity': similar_profiles['ExerciseCapacity'].mean(),
            'age_range': {
                'min': similar_profiles['Age'].min(),
                'max': similar_profiles['Age'].max()
            }
        }

        return insights

    except Exception as e:
        print(f"Error generating insights: {str(e)}")
        return {
            'avg_risk_score': 0,
            'risk_distribution': {},
            'common_diet': 'Unknown',
            'avg_exercise_capacity': 0,
            'age_range': {'min': 0, 'max': 0}
        }