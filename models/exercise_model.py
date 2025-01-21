# models/exercise_model.py
from sklearn.cluster import KMeans
from config import MODEL_CONFIG
from typing import Dict, List
import random


class ExercisePlanGenerator:
    def __init__(self):
        self.kmeans = KMeans(**MODEL_CONFIG['kmeans'])
        self.exercise_database = self._initialize_exercise_database()

    def create_user_clusters(self, data):
        """Create user clusters based on health characteristics"""
        self.kmeans.fit(data)
        return self.kmeans

    def _initialize_exercise_database(self) -> Dict:
        """Initialize the database of exercises for different intensities and goals"""
        return {
            "cardio": {
                "low": [
                    {"name": "Walking", "duration": "20-30 min", "intensity": "Light pace"},
                    {"name": "Swimming", "duration": "15-20 min", "intensity": "Easy stroke"},
                    {"name": "Stationary Bike", "duration": "15-20 min", "intensity": "Low resistance"},
                    {"name": "Elliptical", "duration": "15-20 min", "intensity": "Low resistance"}
                ],
                "moderate": [
                    {"name": "Brisk Walking", "duration": "30-40 min", "intensity": "Moderate pace"},
                    {"name": "Swimming", "duration": "25-30 min", "intensity": "Moderate pace"},
                    {"name": "Cycling", "duration": "30-40 min", "intensity": "Moderate resistance"},
                    {"name": "Rowing", "duration": "20-25 min", "intensity": "Moderate resistance"}
                ],
                "high": [
                    {"name": "Running", "duration": "30-45 min", "intensity": "High pace"},
                    {"name": "HIIT Cardio", "duration": "25-30 min", "intensity": "High intensity intervals"},
                    {"name": "Cycling", "duration": "45-60 min", "intensity": "High resistance"},
                    {"name": "Swimming", "duration": "40-45 min", "intensity": "Fast pace"}
                ]
            },
            "strength": {
                "low": [
                    {"name": "Bodyweight Squats", "sets": "2-3", "reps": "8-10"},
                    {"name": "Wall Push-ups", "sets": "2-3", "reps": "8-10"},
                    {"name": "Chair Dips", "sets": "2-3", "reps": "8-10"},
                    {"name": "Standing Calf Raises", "sets": "2-3", "reps": "12-15"}
                ],
                "moderate": [
                    {"name": "Dumbbell Squats", "sets": "3-4", "reps": "10-12"},
                    {"name": "Push-ups", "sets": "3-4", "reps": "10-12"},
                    {"name": "Dumbbell Rows", "sets": "3-4", "reps": "10-12"},
                    {"name": "Lunges", "sets": "3-4", "reps": "10-12 each leg"}
                ],
                "high": [
                    {"name": "Barbell Squats", "sets": "4-5", "reps": "6-8"},
                    {"name": "Bench Press", "sets": "4-5", "reps": "6-8"},
                    {"name": "Deadlifts", "sets": "4-5", "reps": "6-8"},
                    {"name": "Pull-ups", "sets": "4-5", "reps": "6-8"}
                ]
            },
            "flexibility": {
                "low": [
                    {"name": "Basic Stretching", "duration": "10-15 min"},
                    {"name": "Gentle Yoga", "duration": "15-20 min"},
                    {"name": "Joint Mobility", "duration": "10-15 min"}
                ],
                "moderate": [
                    {"name": "Dynamic Stretching", "duration": "15-20 min"},
                    {"name": "Yoga Flow", "duration": "20-30 min"},
                    {"name": "Pilates", "duration": "20-30 min"}
                ],
                "high": [
                    {"name": "Advanced Yoga", "duration": "45-60 min"},
                    {"name": "Power Stretching", "duration": "30-40 min"},
                    {"name": "Dynamic Mobility Work", "duration": "30-40 min"}
                ]
            }
        }

    def get_weekly_exercise_plan(self, intensity: str, conditions: List[str], goal: str) -> Dict:
        """Generate a 7-day exercise plan based on intensity, conditions, and goals"""
        weekly_plan = {}

        # Define weekly structure based on goal
        if goal == "Weight Loss":
            weekly_structure = [
                {"day": 1, "focus": "Cardio + Strength", "duration": 60},
                {"day": 2, "focus": "Cardio + Flexibility", "duration": 45},
                {"day": 3, "focus": "Strength + Cardio", "duration": 60},
                {"day": 4, "focus": "Rest", "duration": 15},
                {"day": 5, "focus": "Cardio + Strength", "duration": 60},
                {"day": 6, "focus": "Cardio + Flexibility", "duration": 45},
                {"day": 7, "focus": "Rest", "duration": 15}
            ]
        elif goal == "Muscle Gain":
            weekly_structure = [
                {"day": 1, "focus": "Upper Body Strength", "duration": 60},
                {"day": 2, "focus": "Lower Body Strength", "duration": 60},
                {"day": 3, "focus": "Rest", "duration": 15},
                {"day": 4, "focus": "Push Exercises", "duration": 60},
                {"day": 5, "focus": "Pull Exercises", "duration": 60},
                {"day": 6, "focus": "Legs + Core", "duration": 60},
                {"day": 7, "focus": "Rest", "duration": 15}
            ]
        else:  # Maintenance or General Fitness
            weekly_structure = [
                {"day": 1, "focus": "Full Body Strength", "duration": 45},
                {"day": 2, "focus": "Cardio", "duration": 45},
                {"day": 3, "focus": "Flexibility + Core", "duration": 45},
                {"day": 4, "focus": "Rest", "duration": 15},
                {"day": 5, "focus": "Upper Body Strength", "duration": 45},
                {"day": 6, "focus": "Lower Body Strength", "duration": 45},
                {"day": 7, "focus": "Light Cardio + Flexibility", "duration": 30}
            ]

        # Generate exercises for each day
        for day_plan in weekly_structure:
            day = day_plan["day"]
            focus = day_plan["focus"]
            duration = day_plan["duration"]

            if "Rest" in focus:
                exercises = ["Light stretching", "Walking if desired", "Foam rolling"]
                notes = "Focus on recovery and mobility"
            else:
                exercises = self._get_exercises_for_focus(focus, intensity, conditions)
                notes = self._get_exercise_notes(focus, conditions, intensity)

            weekly_plan[day] = {
                "focus": focus,
                "duration": duration,
                "exercises": exercises,
                "notes": notes
            }

        return weekly_plan

    def _get_exercises_for_focus(self, focus: str, intensity: str, conditions: List[str]) -> List[str]:
        """Get appropriate exercises based on the day's focus"""
        exercises = []

        if "Cardio" in focus:
            cardio = random.choice(self.exercise_database["cardio"][intensity])
            exercises.append(f"{cardio['name']} - {cardio['duration']} ({cardio['intensity']})")

        if "Strength" in focus:
            strength_exercises = random.sample(self.exercise_database["strength"][intensity], 3)
            for exercise in strength_exercises:
                exercises.append(f"{exercise['name']} - {exercise['sets']} sets of {exercise['reps']}")

        if "Flexibility" in focus:
            flexibility = random.choice(self.exercise_database["flexibility"][intensity])
            exercises.append(f"{flexibility['name']} - {flexibility['duration']}")

        # Modify exercises based on conditions
        exercises = self._modify_for_conditions(exercises, conditions)

        return exercises

    def _modify_for_conditions(self, exercises: List[str], conditions: List[str]) -> List[str]:
        """Modify exercises based on health conditions"""
        modified_exercises = exercises.copy()

        if "arthritis" in conditions:
            modified_exercises = [ex.replace("Running", "Walking").replace("Jump", "Step")
                                  for ex in modified_exercises]
            modified_exercises.append("Joint mobility exercises")

        if "asthma" in conditions:
            modified_exercises = [ex.replace("HIIT", "Interval").replace("Running", "Brisk Walking")
                                  for ex in modified_exercises]
            modified_exercises.append("Breathing exercises")

        if "hypertension" in conditions:
            modified_exercises = [ex.replace("High intensity", "Moderate intensity")
                                  .replace("Heavy", "Moderate")
                                  for ex in modified_exercises]

        return modified_exercises

    def _get_exercise_notes(self, focus: str, conditions: List[str], intensity: str) -> str:
        """Generate specific notes based on the workout focus and conditions"""
        notes = []

        if "Cardio" in focus:
            notes.append("Monitor heart rate and breathing")
        if "Strength" in focus:
            notes.append("Focus on proper form")
        if "Flexibility" in focus:
            notes.append("Don't bounce in stretches")

        if conditions:
            if "diabetes" in conditions:
                notes.append("Monitor blood sugar levels")
            if "hypertension" in conditions:
                notes.append("Keep intensity moderate and monitor blood pressure")
            if "asthma" in conditions:
                notes.append("Keep inhaler nearby and take breaks as needed")
            if "arthritis" in conditions:
                notes.append("Stop if sharp pain occurs")

        return " | ".join(notes)