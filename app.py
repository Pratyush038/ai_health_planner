import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from models.health_risk_matching import find_similar_profiles, get_profile_insights
from models.health_risk_model import HealthRiskModel, get_risk_level, train_health_risk_model
from models.exercise_model import ExercisePlanGenerator
from models.meal.meal_model import MealPlanGenerator
from utils.data_processing import (
    preprocess_data,
    create_user_features,
    scale_features,
    find_similar_users
)
from config import APP_CONFIG, FEATURES

# Set page configuration
st.set_page_config(
    page_title="HealthAlign",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.2em;
    }
    .health-metric {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .risk-high {
        color: #ff4b4b;
    }
    .risk-moderate {
        color: #ffa500;
    }
    .risk-low {
        color: #00cc00;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header with logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <h1 style='text-align: center; color: #ff4b4b;'>
                🏥 HealthAlign
                <br>
                <span style='font-size: 0.8em; color: #666;'>Your Personalised Health Care Assistant</span>
            </h1>
        """, unsafe_allow_html=True)

    # Initialize session state for models
    if 'health_model' not in st.session_state:
        st.session_state.health_model = None
    if 'exercise_generator' not in st.session_state:
        st.session_state.exercise_generator = None
    if 'meal_generator' not in st.session_state:
        st.session_state.meal_generator = MealPlanGenerator()

    # File uploader with enhanced styling
    st.markdown("### 📊 Training Data Upload")
    uploaded_file = st.file_uploader(
        "Choose a training dataset file",
        type=['csv'],
        help="Upload a CSV file containing health data with required columns"
    )

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
                with st.spinner('Training models... Please wait.'):
                    st.session_state.health_model = train_health_risk_model(data)
                    st.session_state.exercise_generator = ExercisePlanGenerator()
                    st.session_state.exercise_generator.create_user_clusters(data[['Age', 'BMI', 'HealthRiskScore']])
                st.success('Models trained successfully!')

            # Create form for user inputs
            with st.form(key='user_input_form'):
                st.markdown("""
                    <h3 style='color: #333; margin-bottom: 1rem;'>
                        👤 Personal Information
                    </h3>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    # Basic Information
                    st.markdown("#### 📋 Basic Details")
                    selected_age = st.number_input(
                        "Age",
                        min_value=APP_CONFIG['min_age'],
                        max_value=APP_CONFIG['max_age'],
                        value=30,
                        step=1
                    )

                    selected_gender = st.selectbox(
                        "Gender",
                        ['Male', 'Female'],
                        index=0
                    )

                    selected_bmi = st.number_input(
                        "BMI",
                        min_value=APP_CONFIG['min_bmi'],
                        max_value=APP_CONFIG['max_bmi'],
                        value=22.0,
                        step=0.1
                    )

                with col2:
                    # Goals and Activity
                    st.markdown("#### 🎯 Goals & Activity")
                    selected_goal = st.selectbox(
                        "Primary Goal",
                        ["Weight Loss", "Muscle Gain", "Maintenance", "General Fitness"],
                        index=0
                    )

                    activity_level = st.select_slider(
                        "Activity Level",
                        options=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                        value="Moderate"
                    )

                with col3:
                    # Dietary Preferences
                    st.markdown("#### 🥗 Dietary Preferences")
                    dietary_preferences = []
                    for pref in ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"]:
                        if st.checkbox(pref, key=f"diet_{pref}"):
                            dietary_preferences.append(pref.lower())

                # Health conditions in a card-like container
                st.markdown("""
                    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;'>
                        <h4 style='color: #333;'>🏥 Health Conditions</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                conditions = []
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.checkbox("Diabetes"):
                        conditions.append("diabetes")
                with col2:
                    if st.checkbox("Hypertension"):
                        conditions.append("hypertension")
                with col3:
                    if st.checkbox("Asthma"):
                        conditions.append("asthma")

                # Submit button with styling
                submit_button = st.form_submit_button("Generate Your Personalized Health Plan 🚀")

                if submit_button:
                    if st.session_state.health_model is None:
                        st.error("⚠️ Please upload a dataset first!")
                        return

                    try:
                        with st.spinner('Generating your personalized plan...'):
                            # Generate predictions and plans
                            user_features = create_user_features(selected_age, selected_bmi)
                            health_risk = st.session_state.health_model.predict(user_features)[0]
                            risk_level = get_risk_level(health_risk)

                            # Display results in tabs with icons
                            tab1, tab2, tab3 = st.tabs([
                                "🔍 Health Analysis",
                                "🍽 7-Day Meal Plan",
                                "💪 7-Day Exercise Plan"
                            ])

                            with tab1:
                                st.markdown("""
                                    <h3 style='color: #333;'>🤖 AI-Generated Health Analysis</h3>
                                """, unsafe_allow_html=True)
                                
                                # Display risk score in a nice card
                                risk_color = {
                                    "High": "risk-high",
                                    "Moderate": "risk-moderate",
                                    "Low": "risk-low"
                                }[risk_level]
                                
                                st.markdown(f"""
                                    <div class='health-metric'>
                                        <h4>Health Risk Assessment</h4>
                                        <p>Score: <strong>{health_risk:.2f}</strong></p>
                                        <p>Level: <strong class='{risk_color}'>{risk_level}</strong></p>
                                    </div>
                                """, unsafe_allow_html=True)

                                try:
                                    user_profile = {
                                        'Age': selected_age,
                                        'BMI': selected_bmi,
                                        'HealthRiskScore': health_risk
                                    }

                                    similar_profiles = find_similar_profiles(
                                        target_profile=user_profile,
                                        dataset=data,
                                        n_matches=5
                                    )

                                    if similar_profiles is not None and not similar_profiles.empty:
                                        st.markdown("### 👥 Similar Profiles Analysis")
                                        st.markdown("""
                                            <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;'>
                                                Similarity Score indicates how closely these profiles match yours (100 = exact match)
                                            </div>
                                        """, unsafe_allow_html=True)

                                        # Style the dataframe
                                        st.dataframe(
                                            similar_profiles[['Age', 'Gender', 'BMI', 'HealthRiskScore', 'ExerciseCapacity', 'SimilarityScore']],
                                            use_container_width=True,
                                            hide_index=True
                                        )

                                        insights = get_profile_insights(similar_profiles)
                                        
                                        st.markdown("### 📊 Profile Insights")
                                        metrics_col1, metrics_col2 = st.columns(2)
                                        
                                        with metrics_col1:
                                            st.metric("Average Health Risk Score", f"{insights['avg_risk_score']:.1f}")
                                            st.metric("Average Exercise Capacity", f"{insights['avg_exercise_capacity']:.1f}")
                                        
                                        with metrics_col2:
                                            st.metric("Age Range", f"{insights['age_range']['min']} - {insights['age_range']['max']} years")
                                            st.metric("Most Common Diet", insights['common_diet'])

                                    else:
                                        st.warning("⚠️ No similar profiles found. Try adjusting your input parameters.")

                                except Exception as e:
                                    st.error(f"⚠️ Error analyzing similar profiles: {str(e)}")

                            with tab2:
                                st.markdown("### 🍽 Your Personalized 7-Day Meal Plan")
                                meal_plan = st.session_state.meal_generator.generate_meal_plan(
                                    goal=selected_goal,
                                    dietary_preferences=dietary_preferences,
                                    health_conditions=conditions,
                                    risk_level=risk_level
                                )

                                for day, meals in meal_plan.items():
                                    with st.expander(f"Day {day}", expanded=day == "1"):
                                        col1, col2 = st.columns([2, 1])
                                        with col1:
                                            st.markdown(f"""
                                                - 🍳 **Breakfast:** {meals['breakfast']}
                                                - 🥪 **Morning Snack:** {meals['morning_snack']}
                                                - 🥗 **Lunch:** {meals['lunch']}
                                                - 🍎 **Evening Snack:** {meals['evening_snack']}
                                                - 🍽 **Dinner:** {meals['dinner']}
                                            """)
                                        with col2:
                                            st.markdown("### Nutrition Info")
                                            st.markdown(f"**Calories:** {meals['calories']}")
                                            st.markdown(f"**Macros:** {meals['macros']}")

                            with tab3:
                                st.markdown("### 💪 Your Customized 7-Day Exercise Plan")
                                intensity = "low" if risk_level == "High" else "moderate" if risk_level == "Moderate" else "high"
                                exercise_plan = st.session_state.exercise_generator.get_weekly_exercise_plan(
                                    intensity=intensity,
                                    conditions=conditions,
                                    goal=selected_goal
                                )

                                for day, workout in exercise_plan.items():
                                    with st.expander(f"Day {day}", expanded=day == "1"):
                                        col1, col2 = st.columns([3, 1])
                                        with col1:
                                            st.markdown(f"**🎯 Focus:** {workout['focus']}")
                                            st.markdown("**🏋️ Exercises:**")
                                            for exercise in workout['exercises']:
                                                st.markdown(f"- {exercise}")
                                            if workout.get('notes'):
                                                st.info(f"💡 {workout['notes']}")
                                        with col2:
                                            st.markdown(f"**⏱ Duration:** {workout['duration']} minutes")

                    except Exception as e:
                        st.error(f"⚠️ Error generating recommendations: {str(e)}")

        except Exception as e:
            st.error(f"⚠️ Error loading dataset: {str(e)}")

if __name__ == "__main__":
    main()