import pandas as pd
import ast  # To safely evaluate the stringified dictionary
from pprint import pprint


def load_recipes(csv_path):
    """
    Load the recipe dataset from a CSV file.
    """
    return pd.read_csv(csv_path)

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

def search_recipes(recipes_df, target_macros, top_n=10):
    """
    Search for the top N recipes that closely match the target macros.
    """
    weights = {
        "calories": 1.0,
        "protein": 0.5,  # Prioritize protein
        "carbs": 1.0,
        "fats": 2.0,     # Deprioritize fats
    }
    
    results = []
    for _, row in recipes_df.iterrows():
        nutrients = parse_nutrients(row["nutrients"])
        if nutrients:
            deviation = calculate_deviation(nutrients, target_macros, weights)
            results.append((row["name"], row["url"], row["image"], nutrients, deviation))
    
    # Sort results by deviation score
    results = sorted(results, key=lambda x: x[-1])[:top_n]
    return results

# Example Usage
if __name__ == "__main__":
    # User inputs
    daily_macros = {
        "calories": 2842,
        "protein": 173,
        "carbs": 379,
        "fats": 81,
    }
    meals_per_day = 3
    

    # Load dataset
    recipes_csv = "food_dataset\\recipes.csv"
    recipes = load_recipes(recipes_csv)

    # Calculate target macros per meal
    target_macros = {
        "calories": daily_macros["calories"] / meals_per_day,
        "protein": daily_macros["protein"] / meals_per_day,
        "carbs": daily_macros["carbs"] / meals_per_day,
        "fats": daily_macros["fats"] / meals_per_day,
    }

    print(target_macros)

    # Search recipes
    top_recipes = search_recipes(recipes, target_macros)
    pprint(top_recipes)
