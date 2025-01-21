# models/meal_model.py
from typing import Dict, List
import random


class MealPlanGenerator:
    def __init__(self):
        self.meal_database = self._initialize_meal_database()

    def _initialize_meal_database(self) -> Dict:
        """Initialize the database of meals with Indian cuisine focus"""
        return {
            "standard": {
                "breakfast": [
                    "Poha with peanuts and vegetables",
                    "Idli with sambar and chutney",
                    "Masala dosa with coconut chutney",
                    "Upma with vegetables",
                    "Aloo paratha with curd",
                    "Besan chilla with mint chutney",
                    "Oats upma with vegetables"
                ],
                "morning_snacks": [
                    "Fruit chaat",
                    "Roasted chana",
                    "Buttermilk",
                    "Mixed nuts and seeds",
                    "Sprouts bhel",
                    "Masala mathri",
                    "Dates and almonds"
                ],
                "lunch": [
                    "Dal tadka with jeera rice and mixed vegetables",
                    "Rajma chawal with raita",
                    "Chole with brown rice and salad",
                    "Kadhi chawal with aloo gobi",
                    "Matar paneer with roti and salad",
                    "Vegetable biryani with raita",
                    "Dal makhani with jeera rice"
                ],
                "evening_snacks": [
                    "Samosa with green chutney",
                    "Dhokla with chutney",
                    "Bhel puri",
                    "Masala chai with marie biscuits",
                    "Vegetable cutlets",
                    "Corn chaat",
                    "Pani puri"
                ],
                "dinner": [
                    "Mixed vegetable curry with chapati",
                    "Palak paneer with roti",
                    "Dal fry with jeera rice",
                    "Bhindi masala with chapati",
                    "Methi malai matar with paratha",
                    "Vegetable pulao with raita",
                    "Aloo matar with roti"
                ]
            },
            "weight_loss": {
                "breakfast": [
                    "Multigrain dosa with sambar",
                    "Vegetable daliya",
                    "Moong dal chilla",
                    "Ragi idli with chutney",
                    "Sprouts poha",
                    "Oats uttapam",
                    "Quinoa upma"
                ],
                "morning_snacks": [
                    "Mixed sprouts",
                    "Cucumber and carrot sticks",
                    "Chaas (buttermilk)",
                    "Apple with cinnamon",
                    "Roasted makhana",
                    "Green tea with murmura",
                    "Coconut water"
                ],
                "lunch": [
                    "Dal palak with brown rice",
                    "Mixed vegetable curry with millet roti",
                    "Chickpea curry with quinoa",
                    "Moong dal khichdi with vegetables",
                    "Lobia curry with brown rice",
                    "Tofu bhurji with multigrain roti",
                    "Vegetable curry with jowar roti"
                ],
                "evening_snacks": [
                    "Roasted chana chaat",
                    "Steamed corn kernels",
                    "Vegetable soup",
                    "Mixed fruit salad",
                    "Sprouts bhel",
                    "Cucumber raita",
                    "Lemon water with chia seeds"
                ],
                "dinner": [
                    "Lauki curry with chapati",
                    "Mixed dal with vegetable roti",
                    "Spinach soup with multigrain bread",
                    "Tofu curry with millet roti",
                    "Mushroom masala with chapati",
                    "Vegetable daliya khichdi",
                    "Bottle gourd soup with quinoa"
                ]
            },
            "non_vegetarian": {
                "breakfast": [
                    "Egg bhurji with multigrain paratha",
                    "Chicken keema with roti",
                    "Masala omelette with toast",
                    "Fish curry with idli",
                    "Egg white omelette with vegetables",
                    "Chicken sandwich with mint chutney",
                    "Egg rice with vegetables"
                ],
                "morning_snacks": [
                    "Boiled eggs with black pepper",
                    "Chicken tikka",
                    "Fish cutlet",
                    "Egg salad",
                    "Grilled chicken strips",
                    "Tuna sandwich",
                    "Egg bhurji roll"
                ],
                "lunch": [
                    "Chicken curry with brown rice",
                    "Fish curry with chapati",
                    "Mutton curry with jeera rice",
                    "Egg curry with roti",
                    "Chicken biryani with raita",
                    "Fish fry with dal rice",
                    "Keema matar with paratha"
                ],
                "evening_snacks": [
                    "Chicken soup",
                    "Egg bhurji sandwich",
                    "Fish pakora",
                    "Chicken seekh kebab",
                    "Egg rolls",
                    "Grilled fish tikka",
                    "Chicken cutlet"
                ],
                "dinner": [
                    "Grilled chicken with mint chutney",
                    "Fish curry with brown rice",
                    "Egg curry with chapati",
                    "Chicken tikka masala with roti",
                    "Mutton soup with bread",
                    "Tandoori fish with salad",
                    "Chicken stew with appam"
                ]
            }
        }

    def generate_meal_plan(self, goal: str, dietary_preferences: List[str],
                           health_conditions: List[str], risk_level: str) -> Dict:
        """Generate a 7-day Indian meal plan based on user characteristics"""
        meal_plan = {}

        # Select appropriate meal database based on preferences and goals
        if "vegetarian" in dietary_preferences or "vegan" in dietary_preferences:
            if goal == "Weight Loss":
                meals_db = self.meal_database["weight_loss"]
            else:
                meals_db = self.meal_database["standard"]
        else:
            meals_db = self.meal_database["non_vegetarian"]

        # Calculate base calories based on goal
        base_calories = self._calculate_base_calories(goal)

        # Generate plan for each day
        for day in range(1, 8):
            # Select meals for the day
            daily_meals = {
                "breakfast": random.choice(meals_db["breakfast"]),
                "morning_snack": random.choice(meals_db["morning_snacks"]),
                "lunch": random.choice(meals_db["lunch"]),
                "evening_snack": random.choice(meals_db["evening_snacks"]),
                "dinner": random.choice(meals_db["dinner"])
            }

            # Adjust meals based on health conditions
            daily_meals = self._adjust_meals_for_conditions(daily_meals, health_conditions)

            # Calculate macros
            macros = self._calculate_macros(base_calories, goal)

            # Add to meal plan
            meal_plan[day] = {
                **daily_meals,
                "calories": base_calories,
                "macros": macros,
                "notes": self._generate_meal_notes(health_conditions, risk_level)
            }

        return meal_plan

    def _calculate_base_calories(self, goal: str) -> int:
        """Calculate base calories based on goal"""
        base = 2000  # Standard base calories
        if goal == "Weight Loss":
            return base - 500
        elif goal == "Muscle Gain":
            return base + 300
        return base

    def _calculate_macros(self, calories: int, goal: str) -> Dict:
        """Calculate macronutrient distribution"""
        if goal == "Weight Loss":
            return {
                "protein": f"{int(calories * 0.3 / 4)}g (30%)",
                "carbs": f"{int(calories * 0.4 / 4)}g (40%)",
                "fats": f"{int(calories * 0.3 / 9)}g (30%)"
            }
        elif goal == "Muscle Gain":
            return {
                "protein": f"{int(calories * 0.35 / 4)}g (35%)",
                "carbs": f"{int(calories * 0.45 / 4)}g (45%)",
                "fats": f"{int(calories * 0.2 / 9)}g (20%)"
            }
        return {
            "protein": f"{int(calories * 0.25 / 4)}g (25%)",
            "carbs": f"{int(calories * 0.55 / 4)}g (55%)",
            "fats": f"{int(calories * 0.2 / 9)}g (20%)"
        }

    def _adjust_meals_for_conditions(self, meals: Dict, conditions: List[str]) -> Dict:
        """Adjust meals based on health conditions"""
        if "diabetes" in conditions:
            meals = {k: v.replace("white rice", "brown rice")
            .replace("sugar", "stevia")
                     for k, v in meals.items()}
        if "hypertension" in conditions:
            meals = {k: v + " (low sodium)" for k, v in meals.items()}
        if "heart disease" in conditions:
            meals = {k: v.replace("ghee", "olive oil")
            .replace("full fat", "low fat")
                     for k, v in meals.items()}
        return meals

    def _generate_meal_notes(self, conditions: List[str], risk_level: str) -> str:
        """Generate specific notes for the meal plan"""
        notes = []
        if "diabetes" in conditions:
            notes.append("Monitor blood sugar levels after meals")
        if "hypertension" in conditions:
            notes.append("Minimize salt intake")
        if risk_level == "High":
            notes.append("Small, frequent meals recommended")
        return " | ".join(notes) if notes else "Standard Indian diet plan"