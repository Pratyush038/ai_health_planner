🏥 HealthAlign - AI-Powered Health Planner
HealthAlign is an AI-driven health assistant that generates personalized 7-day meal and workout plans based on chronic health conditions. It uses machine learning models, including a nearest neighbor approach on a custom dataset of 10,000 entries, to assess health risks and suggest tailored recommendations.

Features:
Health Risk Assessment – Predicts risk levels using AI models.
Personalized Meal Plans – Custom diet recommendations based on conditions and preferences.
Workout Planning – Adaptive exercise plans suited to risk levels and fitness goals.
Nearest Neighbor Matching – Finds similar health profiles for better insights.

Installation:
git clone https://github.com/Pratyush038/ai_health_planner.git  
cd ai_health_planner  
pip install -r requirements.txt  
streamlit run main.py   

Dataset Requirements
A CSV file with columns: Age, Gender, BMI, HealthRiskScore, ExerciseCapacity.
