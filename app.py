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
    Search for the top N recipes that closely match the target macros.
    """
    # Define weights for each macro
    weights = {
        "calories": 1.0,
        "protein": 0.5,  # Higher priority
        "carbs": 1.0,
        "fats": 2.0,     # Lower priority
    }
    
    results = []
    for _, row in recipes_df.iterrows():
        nutrients = parse_nutrients(row["nutrients"])
        if nutrients:  # Skip recipes with missing/invalid nutrient data
            deviation = calculate_deviation(nutrients, target_macros, weights)
            results.append((row["name"], row["url"], row["image"], nutrients, deviation))
    
    # Sort results by deviation score
    results = sorted(results, key=lambda x: x[-1])[:top_n]
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        calories = int(request.form["calories"])
        protein = int(request.form["protein"])
        carbs = int(request.form["carbs"])
        fats = int(request.form["fats"])
        meals = int(request.form["meals"])

        # Calculate per-meal macros
        target_macros = {
            "calories": calories / meals,
            "protein": protein / meals,
            "carbs": carbs / meals,
            "fats": fats / meals,
        }

        # Search for recipes
        top_recipes = search_recipes(target_macros)

        return render_template("results.html", recipes=top_recipes, target_macros=target_macros)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
