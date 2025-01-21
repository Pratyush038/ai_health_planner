import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from models.health_risk_matching import find_similar_profiles, get_profile_insights
from models.health_risk_model import HealthRiskModel, get_risk_level, train_health_risk_model
from models.exercise_model import ExercisePlanGenerator
from models. meal. meal_model import MealPlanGenerator
from utils.data_processing import (
    preprocess_data,
    create_user_features,
    scale_features,
    find_similar_users
)
from config import APP_CONFIG, FEATURES


def main():
    st.title("HealthAlign - Your Personalised Health Care Assistant")

    # Initialize session state for models
    if 'health_model' not in st.session_state:
        st.session_state.health_model = None
    if 'exercise_generator' not in st.session_state:
        st.session_state.exercise_generator = None
    if 'meal_generator' not in st.session_state:
        st.session_state.meal_generator = MealPlanGenerator()

    # File uploader for dataset
    uploaded_file = st.file_uploader("Choose a training dataset file")

    if uploaded_file:
        try:
            # Load and preprocess data
            data = pd.read_csv(uploaded_file)
            expected_columns = ['Age', 'Gender', 'BMI', 'HealthRiskScore', 'ExerciseCapacity']

            # Verify columns
            if not all(col in data.columns for col in expected_columns):
                st.error(f"Dataset must contain these columns: {', '.join(expected_columns)}")
                return

            data = preprocess_data(data)

            # Initialize models if not already done
            if st.session_state.health_model is None:
                st.session_state.health_model = train_health_risk_model(data)
                st.session_state.exercise_generator = ExercisePlanGenerator()
                st.session_state.exercise_generator.create_user_clusters(data[['Age', 'BMI', 'HealthRiskScore']])

            # Create form for user inputs
            with st.form(key='user_input_form'):
                st.header("Enter Your Information")

                col1, col2 = st.columns(2)

                with col1:
                    # Basic Information
                    selected_age = st.number_input(
                        "Enter age:",
                        min_value=APP_CONFIG['min_age'],
                        max_value=APP_CONFIG['max_age'],
                        value=30,
                        step=1
                    )

                    selected_gender = st.selectbox(
                        "Select gender:",
                        ['Male', 'Female'],
                        index=0
                    )

                    selected_bmi = st.number_input(
                        "Enter BMI:",
                        min_value=APP_CONFIG['min_bmi'],
                        max_value=APP_CONFIG['max_bmi'],
                        value=22.0,
                        step=0.1
                    )

                    selected_goal = st.selectbox(
                        "Select your primary goal:",
                        ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"],
                        index=0
                    )

                with col2:
                    # Dietary Preferences
                    st.subheader("Dietary Preferences")
                    dietary_preferences = []
                    if st.checkbox("Vegetarian"):
                        dietary_preferences.append("vegetarian")
                    if st.checkbox("Vegan"):
                        dietary_preferences.append("vegan")
                    if st.checkbox("Gluten-Free"):
                        dietary_preferences.append("gluten-free")
                    if st.checkbox("Dairy-Free"):
                        dietary_preferences.append("dairy-free")

                    # Activity Level
                    activity_level = st.select_slider(
                        "Activity Level",
                        options=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                        value="Moderate"
                    )

                # Health conditions
                st.subheader("Health Conditions")
                conditions = []
                col1, col2 = st.columns(2)
                with col1:
                    if st.checkbox("Diabetes"):
                        conditions.append("diabetes")
                    if st.checkbox("Hypertension"):
                        conditions.append("hypertension")
                with col2:
                    if st.checkbox("Asthma"):
                        conditions.append("asthma")


                # Submit button
                submit_button = st.form_submit_button("Generate Comprehensive Plan")

                if submit_button:
                    if st.session_state.health_model is None:
                        st.error("Please upload a dataset first!")
                        return

                    try:
                        # Generate predictions and plans
                        user_features = create_user_features(selected_age, selected_bmi)
                        health_risk = st.session_state.health_model.predict(user_features)[0]
                        risk_level = get_risk_level(health_risk)

                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(["Health Analysis", "7-Day Meal Plan", "7-Day Exercise Plan"])

                        with tab1:
                            st.write("### AI-Generated Health Analysis")
                            st.write(f"Predicted Health Risk Score: {health_risk:.2f}")
                            st.write(f"Risk Level: {risk_level}")

                            try:
                                user_profile = {
                                    'Age': selected_age,
                                    'BMI': selected_bmi,
                                    'HealthRiskScore': health_risk
                                }

                                # Verify required columns exist in the dataset
                                required_columns = ['Age', 'Gender', 'BMI', 'HealthRiskScore', 'ExerciseCapacity',
                                                    'DietaryPreference']
                                if not all(col in data.columns for col in required_columns):
                                    st.error(
                                        f"Dataset missing required columns. Required: {', '.join(required_columns)}")
                                    return

                                similar_profiles = find_similar_profiles(
                                    target_profile=user_profile,
                                    dataset=data,
                                    n_matches=5
                                )

                                if similar_profiles is not None and not similar_profiles.empty:
                                    st.write("### Similar Profiles Analysis")
                                    st.write(
                                        "Similarity Score indicates how closely these profiles match yours (100 = exact match)")

                                    # Display only the columns we know exist
                                    display_columns = ['Age', 'Gender', 'BMI', 'HealthRiskScore', 'ExerciseCapacity',
                                                       'SimilarityScore']
                                    st.dataframe(similar_profiles[display_columns])

                                    insights = get_profile_insights(similar_profiles)

                                    st.write("### Profile Insights")
                                    st.write(f"- Average Health Risk Score: {insights['avg_risk_score']:.1f}")
                                    st.write(
                                        f"- Risk Level Distribution: {', '.join([f'{k}: {v}' for k, v in insights['risk_distribution'].items()])}")
                                    st.write(f"- Most Common Dietary Preference: {insights['common_diet']}")
                                    st.write(f"- Average Exercise Capacity: {insights['avg_exercise_capacity']:.1f}")
                                    st.write(
                                        f"- Age Range: {insights['age_range']['min']} - {insights['age_range']['max']} years")
                                else:
                                    st.warning("No similar profiles found. Try adjusting your input parameters.")

                            except Exception as e:
                                st.error(f"Error analyzing similar profiles: {str(e)}")

                        with tab2:
                            st.write("### 7-Day Meal Plan")
                            # Generate meal plan based on user characteristics
                            meal_plan = st.session_state.meal_generator.generate_meal_plan(
                                goal=selected_goal,
                                dietary_preferences=dietary_preferences,
                                health_conditions=conditions,
                                risk_level=risk_level
                            )

                            for day, meals in meal_plan.items():
                                with st.expander(f"Day {day}"):
                                    st.write(f"**Breakfast:** {meals['breakfast']}")
                                    st.write(f"**Morning Snack:** {meals['morning_snack']}")
                                    st.write(f"**Lunch:** {meals['lunch']}")
                                    st.write(f"**Evening Snack:** {meals['evening_snack']}")
                                    st.write(f"**Dinner:** {meals['dinner']}")
                                    st.write(f"**Calories:** {meals['calories']}")
                                    st.write(f"**Macros:** {meals['macros']}")

                        with tab3:
                            st.write("### 7-Day Exercise Plan")
                            # Generate exercise plan based on risk level and conditions
                            intensity = "low" if risk_level == "High" else "moderate" if risk_level == "Moderate" else "high"
                            exercise_plan = st.session_state.exercise_generator.get_weekly_exercise_plan(
                                intensity=intensity,
                                conditions=conditions,
                                goal=selected_goal
                            )

                            for day, workout in exercise_plan.items():
                                with st.expander(f"Day {day}"):
                                    st.write(f"**Focus:** {workout['focus']}")
                                    st.write(f"**Duration:** {workout['duration']} minutes")
                                    st.write("**Exercises:**")
                                    for exercise in workout['exercises']:
                                        st.write(f"- {exercise}")
                                    if workout.get('notes'):
                                        st.info(f"💡 {workout['notes']}")

                    except Exception as e:
                        st.error(f"Error generating recommendations: {str(e)}")

        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")


if __name__ == "__main__":
    main()