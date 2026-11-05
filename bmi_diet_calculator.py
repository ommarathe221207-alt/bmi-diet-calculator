"""BMI & Diet Calculator
A simple command-line tool that calculates BMI, daily calorie needs,
a macro split and a sample meal plan.
For educational use only - not medical advice.
"""

import csv
import os
from datetime import datetime

HISTORY_FILE = "history.csv"

ACTIVITY_LEVELS = {
    "1": ("Sedentary (little or no exercise)", 1.2),
    "2": ("Lightly active (1-3 days/week)", 1.375),
    "3": ("Moderately active (3-5 days/week)", 1.55),
    "4": ("Very active (6-7 days/week)", 1.725),
}

MEAL_PLANS = {
    "veg": {
        "Breakfast": "Oats with milk, banana and nuts",
        "Lunch": "Dal, brown rice, mixed vegetables, curd",
        "Snack": "Fruit bowl or roasted chickpeas",
        "Dinner": "Paneer or tofu wrap with salad",
    },
    "nonveg": {
        "Breakfast": "Eggs, whole-grain toast and fruit",
        "Lunch": "Grilled chicken or fish, rice, vegetables",
        "Snack": "Yogurt with nuts",
        "Dinner": "Chicken or egg curry, chapati, salad",
    },
}


def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmr(weight_kg, height_cm, age, gender):
    """Mifflin-St Jeor equation."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if gender == "m" else base - 161


def calorie_target(tdee, goal, gender):
    """Moderate adjustment with a safety floor."""
    adjust = {"lose": -400, "maintain": 0, "gain": 300}[goal]
    floor = 1500 if gender == "m" else 1200
    return max(tdee + adjust, floor)


def macro_split(calories):
    """Protein 25%, carbs 50%, fat 25% (grams)."""
    return {
        "Protein": round(calories * 0.25 / 4),
        "Carbs": round(calories * 0.50 / 4),
        "Fat": round(calories * 0.25 / 9),
    }


def ask_number(prompt, low, high):
    while True:
        try:
            value = float(input(prompt))
            if low <= value <= high:
                return value
            print(f"Please enter a value between {low} and {high}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def ask_choice(prompt, options):
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return value
        print(f"Please choose one of: {', '.join(options)}")


def save_history(row):
    new_file = not os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["date", "weight_kg", "height_cm", "bmi", "category", "calories"])
        writer.writerow(row)


def main():
    print("=== BMI & Diet Calculator ===\n")
    age = int(ask_number("Age (years): ", 15, 100))
    gender = ask_choice("Gender (m/f): ", ["m", "f"])
    weight = ask_number("Weight (kg): ", 30, 250)
    height = ask_number("Height (cm): ", 120, 230)

    print("\nActivity level:")
    for key, (label, _) in ACTIVITY_LEVELS.items():
        print(f"  {key}. {label}")
    activity = ask_choice("Choose (1-4): ", list(ACTIVITY_LEVELS))
    goal = ask_choice("Goal (lose/maintain/gain): ", ["lose", "maintain", "gain"])
    diet = ask_choice("Diet type (veg/nonveg): ", ["veg", "nonveg"])

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * ACTIVITY_LEVELS[activity][1]
    calories = round(calorie_target(tdee, goal, gender))
    macros = macro_split(calories)

    print("\n--- Your Results ---")
    print(f"BMI: {bmi:.1f} ({category})")
    print(f"Maintenance calories: {round(tdee)} kcal/day")
    print(f"Suggested intake for goal '{goal}': {calories} kcal/day")
    print("Macros (grams/day): " + ", ".join(f"{k} {v}g" for k, v in macros.items()))

    print("\nSample meal plan:")
    for meal, food in MEAL_PLANS[diet].items():
        print(f"  {meal}: {food}")

    if category == "Underweight" and goal == "lose":
        print("\nNote: your BMI is in the underweight range. Please consult a doctor.")
    print("\nDisclaimer: educational tool only. Consult a doctor or dietitian.")

    save_history([datetime.now().strftime("%Y-%m-%d %H:%M"), weight, height,
                  round(bmi, 1), category, calories])
    print(f"Result saved to {HISTORY_FILE}")


if __name__ == "__main__":
    main()
