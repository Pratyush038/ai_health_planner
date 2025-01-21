import pandas as pd
import numpy as np
from typing import List, Tuple


def generate_health_dataset(n_samples: int = 10000) -> pd.DataFrame:
    """
    Generate synthetic health dataset with realistic distributions

    Parameters:
    n_samples (int): Number of samples to generate

    Returns:
    pd.DataFrame: Generated dataset
    """
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate age (normal distribution centered around 35)
    age = np.random.normal(35, 12, n_samples)
    age = np.clip(age, 18, 80).astype(int)

    # Generate gender (roughly 50-50 split)
    gender = np.random.choice(['Male', 'Female'], n_samples)

    # Generate BMI (normal distribution with realistic parameters)
    bmi = np.random.normal(25, 4, n_samples)
    bmi = np.clip(bmi, 16, 40).round(1)  # Clip to realistic BMI range

    # Generate health risk score (influenced by age and BMI)
    health_risk = np.zeros(n_samples)
    for i in range(n_samples):
        # Base risk
        base_risk = np.random.normal(50, 15)

        # Age factor (higher risk with age)
        age_factor = (age[i] - 18) / 62 * 30  # Max 30 points from age

        # BMI factor (higher risk for very low or very high BMI)
        bmi_factor = abs(bmi[i] - 22) * 2  # Optimal BMI around 22

        # Combine factors
        total_risk = base_risk + age_factor + bmi_factor
        health_risk[i] = np.clip(total_risk, 0, 100).round(1)

    # Generate exercise capacity (inversely related to health risk)
    exercise_capacity = np.zeros(n_samples)
    for i in range(n_samples):
        # Base capacity
        base_capacity = 100 - health_risk[i]

        # Add some random variation
        variation = np.random.normal(0, 10)

        exercise_capacity[i] = np.clip(base_capacity + variation, 0, 100).round(1)

    # Generate dietary preferences
    preferences = ['Standard', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free']
    weights = [0.6, 0.15, 0.1, 0.1, 0.05]  # Probability distribution
    dietary_preference = np.random.choice(preferences, n_samples, p=weights)

    # Create DataFrame
    df = pd.DataFrame({
        'Age': age,
        'Gender': gender,
        'BMI': bmi,
        'HealthRiskScore': health_risk,
        'ExerciseCapacity': exercise_capacity,
        'DietaryPreference': dietary_preference
    })

    return df


# Generate the dataset
dataset = generate_health_dataset(10000)


# Add some correlations and patterns
def adjust_for_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Add realistic patterns and correlations to the dataset"""

    # Adjust exercise capacity based on age
    df['ExerciseCapacity'] = df.apply(
        lambda row: max(0, row['ExerciseCapacity'] - (row['Age'] - 18) * 0.3),
        axis=1
    )

    # Adjust health risk for dietary preferences
    diet_risk_factors = {
        'Standard': 0,
        'Vegetarian': -2,
        'Vegan': -3,
        'Gluten-Free': -1,
        'Dairy-Free': -1
    }

    df['HealthRiskScore'] = df.apply(
        lambda row: max(0, row['HealthRiskScore'] + diet_risk_factors[row['DietaryPreference']]),
        axis=1
    )

    return df


# Apply patterns and save dataset
final_dataset = adjust_for_patterns(dataset)
final_dataset.to_csv('health_fitness_dataset.csv', index=False)

# Print summary statistics
print("\nDataset Summary:")
print("-" * 50)
print(final_dataset.describe())
print("\nValue Counts:")
print("-" * 50)
print("\nGender Distribution:")
print(final_dataset['Gender'].value_counts(normalize=True))
print("\nDietary Preference Distribution:")
print(final_dataset['DietaryPreference'].value_counts(normalize=True))