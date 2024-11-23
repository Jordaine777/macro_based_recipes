from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load dataset
recipes_csv = "food_dataset\\recipes.csv"
recipes_df = pd.read_csv(recipes_csv)

def parse_nutrients(nutrient_str):
    """
    Parse the nutrients column into a dictionary and extract macros.
    """
    if not isinstance(nutrient_str, str) or nutrient_str.strip() == "":
        return None  # Return None for empty or invalid nutrient data

    try:
        # Convert stringified dictionary into a Python dictionary
        nutrients = ast.literal_eval(nutrient_str)
        # Extract and clean macro values
        macros = {
            "calories": float(nutrients.get("kcal", "0").replace("g", "")),
            "protein": float(nutrients.get("protein", "0").replace("g", "")),
            "carbs": float(nutrients.get("carbs", "0").replace("g", "")),
            "fats": float(nutrients.get("fat", "0").replace("g", ""))
        }
        return macros
    except (ValueError, SyntaxError):
        return None  # Return None for invalid parsing

def calculate_deviation(recipe_macros, target_macros, weights):
    """
    Calculate the weighted deviation score for a recipe based on the target macros.
    """
    return sum(
        weights.get(macro, 1.0) * abs(recipe_macros.get(macro, 0) - target_macros.get(macro, 0))
        for macro in target_macros
    )

def search_recipes(target_macros, top_n=10):
    """
    Search for the top N unique recipes that closely match the target macros.
    """
    weights = {
        "calories": 1.0,
        "protein": 2.0,  # Higher priority
        "carbs": 1.0,
        "fats": 0.5,     # Lower priority
    }

    results = []
    seen_names = set()  # Track unique recipe names

    for _, row in recipes_df.iterrows():
        nutrients = parse_nutrients(row["nutrients"])
        if nutrients and row["name"] not in seen_names:  # Ensure uniqueness by name
            deviation = calculate_deviation(nutrients, target_macros, weights)
            results.append((row["name"], row["url"], row["image"], nutrients, deviation))
            seen_names.add(row["name"])  # Add name to the seen set

    # Sort results by deviation score
    sorted_results = sorted(results, key=lambda x: x[-1])[:top_n]

    # Return the structure expected by the template
    return [(recipe[0], recipe[1], recipe[2], recipe[3]) for recipe in sorted_results]



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        calories = int(request.form["calories"])
        protein = int(request.form["protein"])
        carbs = int(request.form["carbs"])
        fats = int(request.form["fats"])
        meals = int(request.form["meals"])

        # Calculate per-meal macros and round to whole numbers
        target_macros = {
            "calories": round(calories / meals),
            "protein": round(protein / meals),
            "carbs": round(carbs / meals),
            "fats": round(fats / meals),
        }

        # Search for recipes
        top_recipes = search_recipes(target_macros)

        return render_template("results.html", recipes=top_recipes, target_macros=target_macros)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
