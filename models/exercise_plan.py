import numpy as np
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class WorkoutParameters:
    age: int
    gender: str
    conditions: List[str]
    fitness_level: str = "moderate"


class AIWorkoutPlanGenerator:
    def __init__(self):
        self.exercise_library = {
            'cardio': {
                'low': ['Walking', 'Light swimming', 'Stationary cycling (low resistance)'],
                'moderate': ['Brisk walking', 'Swimming', 'Cycling', 'Elliptical'],
                'high': ['Jogging', 'Running', 'High-intensity cycling', 'Swimming laps']
            },
            'strength': {
                'low': ['Body weight squats', 'Wall push-ups', 'Seated rows with resistance band'],
                'moderate': ['Dumbbell squats', 'Regular push-ups', 'Resistance band workouts'],
                'high': ['Barbell squats', 'Advanced push-ups', 'Pull-ups']
            },
            'flexibility': {
                'low': ['Gentle stretching', 'Basic yoga', 'Range of motion exercises'],
                'moderate': ['Yoga flow', 'Dynamic stretching', 'Pilates'],
                'high': ['Power yoga', 'Advanced stretching', 'Dynamic flexibility work']
            }
        }

    def _calculate_intensity(self, params: WorkoutParameters) -> str:
        """Calculate workout intensity based on age and conditions"""
        base_score = 100

        # Age factor
        if params.age < 30:
            age_penalty = 0
        elif params.age < 50:
            age_penalty = (params.age - 30) * 1.5
        else:
            age_penalty = 30 + (params.age - 50) * 2

        # Health conditions factor
        condition_penalty = len(params.conditions) * 15

        # Calculate final score
        final_score = base_score - age_penalty - condition_penalty

        if final_score > 70:
            return 'high'
        elif final_score > 40:
            return 'moderate'
        else:
            return 'low'

    def _adjust_for_conditions(self, exercises: List[str], conditions: List[str]) -> List[str]:
        """Modify exercises based on health conditions"""
        adjustments = {
            'diabetes': {
                'Running': 'Brisk walking',
                'High-intensity cycling': 'Moderate cycling',
                'Barbell squats': 'Body weight squats'
            },
            'hypertension': {
                'Running': 'Walking',
                'High-intensity cycling': 'Light cycling',
                'Advanced push-ups': 'Wall push-ups'
            },
            'asthma': {
                'Running': 'Walking',
                'High-intensity cycling': 'Light cycling',
                'Power yoga': 'Gentle yoga'
            },
            'arthritis': {
                'Running': 'Swimming',
                'Barbell squats': 'Water aerobics',
                'Push-ups': 'Resistance band exercises'
            }
        }

        adjusted_exercises = exercises.copy()
        for condition in conditions:
            if condition in adjustments:
                for i, exercise in enumerate(adjusted_exercises):
                    for original, replacement in adjustments[condition].items():
                        if original in exercise:
                            adjusted_exercises[i] = replacement

        return adjusted_exercises

    def _generate_day_plan(self, intensity: str, focus: str) -> Dict:
        """Generate a single day's workout plan"""
        exercises = []
        duration = 0

        if intensity == 'low':
            duration = 30
            exercises = [
                np.random.choice(self.exercise_library[focus]['low']),
                np.random.choice(self.exercise_library['flexibility']['low'])
            ]
        elif intensity == 'moderate':
            duration = 45
            exercises = [
                np.random.choice(self.exercise_library[focus]['moderate']),
                np.random.choice(self.exercise_library['strength']['moderate']),
                np.random.choice(self.exercise_library['flexibility']['moderate'])
            ]
        else:
            duration = 60
            exercises = [
                np.random.choice(self.exercise_library[focus]['high']),
                np.random.choice(self.exercise_library['strength']['high']),
                np.random.choice(self.exercise_library['flexibility']['high'])
            ]

        return {
            'duration': duration,
            'exercises': exercises
        }

    def generate_weekly_plan(self, params: WorkoutParameters) -> Dict:
        """Generate a complete 7-day workout plan"""
        intensity = self._calculate_intensity(params)

        # Define weekly focus
        weekly_focus = {
            1: 'cardio',
            2: 'strength',
            3: 'cardio',
            4: 'strength',
            5: 'cardio',
            6: 'flexibility',
            7: 'rest'
        }

        weekly_plan = {}
        for day in range(1, 8):
            if weekly_focus[day] == 'rest':
                weekly_plan[f'Day {day}'] = {
                    'duration': 0,
                    'exercises': ['Rest and Recovery', 'Light stretching'],
                    'notes': 'Focus on recovery and gentle movement'
                }
                continue

            day_plan = self._generate_day_plan(intensity, weekly_focus[day])

            # Adjust exercises based on health conditions
            adjusted_exercises = self._adjust_for_conditions(day_plan['exercises'], params.conditions)

            weekly_plan[f'Day {day}'] = {
                'duration': day_plan['duration'],
                'exercises': adjusted_exercises,
                'notes': f"Focus on {weekly_focus[day]}"
            }

        return weekly_plan


# Example usage in your Streamlit app
def get_workout_plan(age: int, gender: str, conditions: List[str]) -> Dict:
    planner = AIWorkoutPlanGenerator()
    params = WorkoutParameters(age=age, gender=gender, conditions=conditions)
    return planner.generate_weekly_plan(params)